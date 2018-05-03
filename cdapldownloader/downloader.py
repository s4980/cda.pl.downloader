import requests
from tqdm import tqdm
import math

from os import path
from urllib.error import HTTPError, URLError

import mimetypes


class Downloader:
    def __init__(self, domain, user, dest_folder, dry_run=False):
        self.domain = domain
        self.user = user
        self.user_folder_url = path.join(self.domain, self.user, 'folder')
        self.dest_folder = dest_folder
        self.dry_run = dry_run

    def get_page_source(self, folder_path):
        try:
            # folder_path = path.join(self.user_folder_url, folder)
            page = requests.get(folder_path)
            return page.content
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

    def download_video(self, video):
        # Get page headers
        headers = requests.head(video.download_url)

        # Total size in bytes.
        total_size = int(headers.headers['content-length'])
        block_size = 1024
        wrote = 0

        # File extension
        if video.file_name is None:
            video.set_file_name(self.get_video_extention(video.download_url))

        # Open stream
        response = requests.get(video.download_url, stream=True)

        # Download video with progress bar
        video_dest_path = path.join(self.dest_folder, video.file_name)
        with open(video_dest_path, 'wb') as out_file:
            for data in tqdm(response.iter_content(block_size),
                             total=math.ceil(total_size // block_size),
                             unit='KB',
                             unit_scale=True):
                wrote = wrote + len(data)
                out_file.write(data)
        if total_size != 0 and wrote != total_size:
            print("ERROR, something went wrong")
        del response
        print(f'Video saved to {video_dest_path}')

    def get_video_extention(self, video_download_url):
        # Get page headers
        headers = requests.head(video_download_url)
        # File extension
        return mimetypes.guess_extension(headers.headers['content-type'])
