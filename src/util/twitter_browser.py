import time

import chromedriver_autoinstaller

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



chromedriver_autoinstaller.install()

class Browser():
    OPTIONS = Options()
    OPTIONS.add_argument('--no-sandbox')
    OPTIONS.add_argument('--window-size=1420,1080')
    # OPTIONS.add_argument('--headless')
    OPTIONS.add_argument('--disable-gpu')

    DRIVER_PATH = './chromedriver.exe'
        
    def __init__(self, url) -> None:
        self.url = url
        self.browser = webdriver.Chrome(executable_path=self.DRIVER_PATH, options=self.OPTIONS)
        self.browser.get(self.url)
        time.sleep(5)
        print('webpage opened in background')
  
    def close(self):
        self.browser.close()


class TwitterBrowser(Browser):

    def __init__(self, url) -> None:
        super().__init__(url=url)
        
    def get_user_birthday(self):
        birthday_xpath = '//span[@data-testid="UserBirthdate"]'
        birthdays = self.browser.find_elements(By.XPATH, birthday_xpath)
        birthday_texts = [
            birthday.text for birthday in birthdays
            ]
        return birthday_texts[0] if birthday_texts else None