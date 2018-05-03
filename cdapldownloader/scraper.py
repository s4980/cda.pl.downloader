from lxml import html
from selenium.common.exceptions import WebDriverException


def detect_subfolders(page_source):
    """
    Detects if there are sub-folders on the page
    :param page_source: html page source
    :return: List of sub-folders urls or empty if none are found
    """
    tree = get_page_source_tree(page_source)
    # //div[@title = 'title']//li/p[. = 'Some Text 1']/following-sibling::span[1]
    return tree.xpath('//span[@class="folder-area"]//a[@class="object-folder blur"]/@href')
    # if len(folder_elements) == 0:
    #     return folder_elements
    # else:
    #     subfolders = defaultdict()
    #     for element in folder_elements:
    #         href = element.xpath('//a').get_attribute('href')
    #         text = element.xpath('//span[@class="name-folder"]/text()')
    #         subfolders[href] = text
    #     return subfolders


def get_video_download_url(video_page, web_driver):
    try:
        web_driver.driver.get(video_page)
        video_player = web_driver.driver.find_element_by_xpath('//video[@class="pb-video-player"]')
        return video_player.get_attribute('src')
    except WebDriverException:
        return None


def get_folder_name(page_source, folder_page_url):
    tree = get_page_source_tree(page_source)
    return tree.xpath(f'//a[@href="{folder_page_url}" and not(@class="active")]/text()')[0]


def get_thumbnails(page_source):
    tree = get_page_source_tree(page_source)
    return tree.xpath('//a[@class="link-title-visit"]')


def get_page_source_tree(page_source: str) -> object:
    tree = html.fromstring(page_source)
    return tree
