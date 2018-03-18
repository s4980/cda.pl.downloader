import requests
from tqdm import tqdm
import math

from os import path
from urllib.error import HTTPError, URLError

import mimetypes


class Downloader:
    def __init__(self, domain, user):
        self.domain = domain
        self.user = user
        self.user_folder = path.join(self.domain, self.user, 'folder')

    def get_page_source(self, folder):
        try:
            folder_path = path.join(self.user_folder, folder)
            page = requests.get(folder_path)
            return page.content
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)


def download_video(video):
    # Get page headers
    headers = requests.head(video.download_url)

    # Total size in bytes.
    total_size = int(headers.headers['content-length'])
    block_size = 1024
    wrote = 0

    # File extension
    video_extension = mimetypes.guess_extension(headers.headers['content-type'])

    # Open stream
    response = requests.get(video.download_url, stream=True)

    # Download video with progress bar
    video_file = '{}{}'.format(video.title, video_extension)
    with open(video_file, 'wb') as out_file:
        for data in tqdm(response.iter_content(block_size),
                         total=math.ceil(total_size // block_size),
                         unit='KB',
                         unit_scale=True):
            wrote = wrote + len(data)
            out_file.write(data)
    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")
    del response
    print('Video saved to {}'.format(video_file))
