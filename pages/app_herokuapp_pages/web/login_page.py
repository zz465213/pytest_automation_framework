import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.allure_factory import AllureFactory


class LoginPage(BasePage):
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BTN = (By.XPATH, "//button[@type='submit']")
    LOGGING_PAGE_TITLE = (By.XPATH, "//div[@id='content']//h2")

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.allure_factory = AllureFactory()

    def user_login(self, username, password):
        """
        1. 輸入帳號密碼進入登入頁
        2. 取得登入首頁標題文字
        """
        self.allure_factory.add_test_step(f"輸入帳號: {username}, 密碼:***")
        self.input_text(self.USERNAME_FIELD, username)
        self.input_text(self.PASSWORD_FIELD, password)
        self.click_element(self.LOGIN_BTN)
        return self.get_text(self.LOGGING_PAGE_TITLE)
