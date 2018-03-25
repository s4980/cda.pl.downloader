from os import path
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def get_video_download_url(video_page):
    chrome_options = Options()
    chrome_options.add_argument('--allow-outdated-plugins')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options,
                              executable_path=path.join(path.dirname(path.realpath(__file__)), 'chromedriver'))
    driver.get(video_page)

    try:
        video_player = driver.find_element_by_xpath('//video[@class="pb-video-player"]')
        return video_player.get_attribute('src')
    except WebDriverException:
        return None
    finally:
        driver.quit()


def get_folder_name(page_source, folder_page_url):
    tree = html.fromstring(page_source)
    return tree.xpath('//a[@href="{}" and not(@class="active")]/text()'.format(folder_page_url))[0]


def get_thumbnails(page_source):
    tree = html.fromstring(page_source)
    return tree.xpath('//a[@class="link-title-visit"]')
