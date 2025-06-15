import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.allure_factory import AllureFactory


class KKTIXPortalPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.logger = logging.getLogger(__name__)
        self.allure_factory = AllureFactory()
        self.driver = driver
        self.url = url
