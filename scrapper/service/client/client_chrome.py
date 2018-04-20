import logging
import os
from time import time

from scrapper.service.client.driver import Driver

SUPREJOB_LOGIN_XPATH = r'//*[@id="app"]/div/div/div[2]/div[2]/div/div[3]/form/div[1]/label/input'
SUPREJOB_PASS_XPATH = r'//*[@id="app"]/div/div/div[2]/div[2]/div/div[3]/form/div[2]/div/label/input'
SUPREJOB_LOGIN_BUTTON = r'//*[@id="app"]/div/div/div[2]/div[2]/div/div[3]/form/button'


class SuperjobClient:
    url_login = r'https://www.superjob.ru/auth/login'
    app_secret = r''

    def __init__(self):
        super().__init__()
        self.driver = Driver.get_instance()
        self.log = logging.getLogger('console')

    def login(self):
        print(self.driver.execute_script("return navigator.userAgent"))
        self.driver.get(self.url_login)
        self.driver.find_element_by_xpath(SUPREJOB_LOGIN_XPATH).send_keys("2668211")
        self.driver.find_element_by_xpath(SUPREJOB_PASS_XPATH).send_keys("wl9274")
        self.driver.find_element_by_xpath(SUPREJOB_LOGIN_BUTTON).click()

        print(self.driver.current_url)
        self.driver.get_screenshot_as_file(os.path.join('files', 'Superjob-'+str(time()+'.png')))
