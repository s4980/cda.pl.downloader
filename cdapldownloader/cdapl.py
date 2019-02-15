from typing import List, Any

from cdapldownloader import scraper
from collections import defaultdict

from cdapldownloader.downloader import Downloader
from cdapldownloader.scraper import get_folder_name, get_thumbnails, get_video_download_url, detect_pagination
from cdapldownloader.utils import query_yes_no
from cdapldownloader.video import Video
from cdapldownloader.web_driver import WebDriver


def get_all_pages(folder_url, downloader):
    sources = list()
    page_source = downloader.get_page_source(folder_url)
    sources.append(page_source)
    next_page_url = detect_pagination(page_source)
    while next_page_url is not None:
        page_source = downloader.get_page_source(next_page_url)
        sources.append(page_source)
        next_page_url = detect_pagination(page_source)
    return sources


def get_all_subfolders(sources: list):
    """
    From list of source pages (folder page type) creates a list of subfolder/video urls
    :param sources: list of html page sources
    :return: list of subfolders urls
    """
    subfolders: List[str] = list()
    for source in sources:
        subfolders.append(scraper.detect_subfolders(source))
    return subfolders


def download_videos_from_subfolders(cda_folder_urls: list, downloader: Downloader):
    web_driver = WebDriver()
    try:
        for cda_folder in cda_folder_urls:
            # Get User's main page html source
            source = downloader.get_page_source(cda_folder)
            # Add User's main folder to subfolders list
            subfolders: List[str] = list()
            subfolders.append(cda_folder)
            # Get all subfolders from Foldery section on User's main page
            subfolders.extend(scraper.detect_subfolders(source))
            # If there is more than main folder (Folder główny) iterate over them and collect all videos from this subfolders
            if len(subfolders) > 0:
                for video_folder in subfolders:
                    download_videos_from_folder(video_folder, downloader, web_driver)
            else:
                download_videos_from_folder(cda_folder, downloader, web_driver)
    finally:
        web_driver.close()


def download_videos_from_folder(cda_video_folder, downloader: Downloader, web_driver):
    video_folders = defaultdict(list)

    # Get page source
    # source = downloader.get_page_source(cda_video_folder)

    # Check if folder is paginated. If there are more pages get the page sources.
    # Later collect video details from all pages
    for source in get_all_pages(cda_video_folder, downloader):
        # Get video details form thumbnails
        for thumbnail in get_thumbnails(source):
            folder_name = get_folder_name(source, cda_video_folder)
            video_folders[folder_name].append(Video(thumbnail.text, thumbnail.attrib['href']))

    # Download videos from cda_video_folder pages
    for folder in video_folders:
        if query_yes_no(f"Download from {'current folder' if folder is None else {folder}} [{len(video_folders[folder])}] ?"):
            if not downloader.dry_run:
                print(f"Getting videos from {'current folder' if folder is None else '{folder}'}")
            for video in video_folders[folder]:
                if query_yes_no(f"\t{video.title} - download ?"):
                    print("\n\t\tDetecting video url. This might take few seconds ...")
                    video.download_url = get_video_download_url(video.page_url, web_driver)
                    if video.download_url is None:
                        print("\t\tUnable to detect video url. Aborting download.")
                        continue
                    video.set_file_name(downloader.get_video_extension(video.download_url))
                    if downloader.dry_run:
                        print(video.download_url, video.file_name)
                    else:
                        print(f"\t\tVideo details:\n\t\t\t{video.__str__}")
                        downloader.download_video(video)
                else:
                    continue
