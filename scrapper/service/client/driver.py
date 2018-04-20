import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from app.settings import BASE_DIR


DRIVER_PATH = os.path.join(BASE_DIR, 'bin', 'chromedriver_2.36')
USER_AGENT = r'user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'


class Driver:
    @staticmethod
    def get_instance():
        options = Options()
        options.add_argument('--window-size=720x550')
        options.add_argument(USER_AGENT)
        driver_path = os.path.join(BASE_DIR, 'bin', 'chromedriver_2.36')

        driver = webdriver.Chrome(chrome_options=options, executable_path=driver_path)
        driver.set_window_size(720, 550)

        return driver
