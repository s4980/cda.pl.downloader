from os import path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--allow-outdated-plugins')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options,
                                       executable_path=path.join(path.dirname(path.realpath(__file__)), 'chromedriver'))

    def close(self):
        self.driver.close()
