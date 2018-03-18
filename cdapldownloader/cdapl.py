from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import os

from selenium.common.exceptions import WebDriverException

from cdapldownloader.downloader import Downloader, download_video
from lxml import html
from collections import defaultdict

from cdapldownloader.video import Video


def get_video_download_url(video_page):
    chrome_options = Options()
    chrome_options.add_argument('--allow-outdated-plugins')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver'))
    driver.get(video_page)

    try:
        video_player = driver.find_element_by_xpath('//video[@class="pb-video-player"]')
        return video_player.get_attribute('src')
    except WebDriverException:
        return ''
    finally:
        driver.quit()


def download_videos(params):
    user = params['cda_user']
    domain = params['cda_domain']
    downloader = Downloader(domain, user)
    video_folders = defaultdict(list)
    for folder in params['cda_folders']:
        source = downloader.get_page_source(folder)
        tree = html.fromstring(source)
        folder_name = \
            tree.xpath(
                '//a[@href="{}" and not(@class="active")]/text()'.format(os.path.join(downloader.user_folder, folder)))[
                0]
        thumbnails = tree.xpath('//a[@class="link-title-visit"]')
        for thumbnail in thumbnails:
            video_folders[folder_name].append(Video(thumbnail.text, thumbnail.attrib['href']))
    for folder in video_folders:
        print(folder)
        for video in video_folders[folder]:
            video.download_url = get_video_download_url(video.page_url)
            print(video)
            download_video(video)
