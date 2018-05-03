from cdapldownloader import scraper
from collections import defaultdict
from cdapldownloader.scraper import get_folder_name, get_thumbnails, get_video_download_url
from cdapldownloader.utils import query_yes_no
from cdapldownloader.video import Video
from cdapldownloader.web_driver import WebDriver


def download_videos_from_subfolders(cda_folder_urls, downloader):
    web_driver = WebDriver()
    try:
        for cda_folder in cda_folder_urls:
            source = downloader.get_page_source(cda_folder)
            subfolders = scraper.detect_subfolders(source)
            if len(subfolders) > 0:
                for video_folder in subfolders:
                    download_videos_from_folder(video_folder, downloader, web_driver)
            else:
                download_videos_from_folder(cda_folder, downloader, web_driver)
    finally:
        web_driver.close()


def download_videos_from_folder(cda_folder, downloader, web_driver):
    video_folders = defaultdict(list)

    # Get page source
    source = downloader.get_page_source(cda_folder)

    # Get video details form thumbnails
    for thumbnail in get_thumbnails(source):
        folder_name = get_folder_name(source, cda_folder)
        video_folders[folder_name].append(Video(thumbnail.text, thumbnail.attrib['href']))

    # Download videos from cda_folder page
    for folder in video_folders:
        if query_yes_no(f"Download '{folder}' ?"):
            if not downloader.dry_run:
                print(folder)
            for video in video_folders[folder]:
                video.download_url = get_video_download_url(video.page_url, web_driver)
                if video.download_url is None:
                    continue
                video.set_file_name(downloader.get_video_extention(video.download_url))
                if downloader.dry_run:
                    print(video.download_url, video.file_name)
                else:
                    print(video)
                    downloader.download_video(video)
