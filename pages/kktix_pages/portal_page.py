import logging
from pages.base_page import BasePage
from utils.allure_factory import AllureFactory


class KKTIXPortalPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.allure_factory = AllureFactory()
        self.driver = driver
