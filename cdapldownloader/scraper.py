from typing import Optional, Any

from lxml import html
from selenium.common.exceptions import WebDriverException


def detect_subfolders(page_source: str):
    """
    Detects if there are sub-folders on the page
    :param page_source: html page source
    :return: List of sub-folders urls or empty if none are found
    """
    tree = get_page_source_tree(page_source)
    return tree.xpath('//span[@class="folder-area"]//a[@class="object-folder blur"]/@href')


def get_video_download_url(video_page, web_driver) -> Optional[Any]:
    try:
        web_driver.driver.get(video_page)
        video_player = web_driver.driver.find_element_by_xpath('//video[@class="pb-video-player"]')
        return video_player.get_attribute('src')
    except WebDriverException:
        return None


def get_folder_name(page_source, folder_page_url):
    tree = get_page_source_tree(page_source)
    folder_tag = tree.xpath(f"//a[@href=\"{folder_page_url}\" and not(@class=\"active\")]/text()")
    if len(folder_tag) > 0:
        return folder_tag[0]
    else:
        return None


def get_thumbnails(page_source):
    tree = get_page_source_tree(page_source)
    return tree.xpath('//a[@class="link-title-visit"]')


def get_page_source_tree(page_source: str) -> object:
    tree = html.fromstring(page_source)
    return tree


def detect_pagination(page_source: str):
    """
    Detects if current folder has more than one page
    :param page_source: html page source
    :return: url link to next page if exists
    """
    tree = get_page_source_tree(page_source)
    hrefs = tree.xpath('//div[@class="paginationControl"]//a[@class="btn btn-primary block"]/@href')
    if len(hrefs) > 0:
        return hrefs[0]
    else:
        return None
