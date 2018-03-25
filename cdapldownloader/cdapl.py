from os import path

from cdapldownloader.downloader import Downloader

from collections import defaultdict

from cdapldownloader.scraper import get_folder_name, get_thumbnails, get_video_download_url
from cdapldownloader.video import Video


def download_videos(params):
    downloader = Downloader(params['cda_domain'], params['cda_user'])
    video_folders = defaultdict(list)
    for folder in params['cda_folders']:
        source = downloader.get_page_source(folder)
        for thumbnail in get_thumbnails(source):
            folder_name = get_folder_name(source, path.join(downloader.user_folder_url, folder))
            video_folders[folder_name].append(Video(thumbnail.text, thumbnail.attrib['href']))
    for folder in video_folders:
        print(folder)
        for video in video_folders[folder]:
            video.download_url = get_video_download_url(video.page_url)
            video.set_file_name(downloader.get_video_extention(video.download_url))
            if params['dry_run']:
                print(video.download_url, video.file_name)
            else:
                print(video)
                downloader.download_video(video)
