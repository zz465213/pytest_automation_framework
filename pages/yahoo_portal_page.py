from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.allure_factory import AllureFactory


class YahooPortalPage(BasePage):
    SEARCH_INPUT = (By.ID, "header-search-input")
    SEARCH_BTN = (By.ID, "header-desktop-search-button")
    SEARCH_RESULT_TITLE = (By.XPATH, "//h3/span[@class=' fz-20 lh-26 d-b tc']")

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.allure_factory = AllureFactory()
        self.driver = driver
        self.url = url

    def search_result(self, text):
        """執行登入操作"""
        self.allure_factory.add_test_step(f"搜尋內容: {text}")
        self.input_text(self.SEARCH_INPUT, text)
        self.click_element(self.SEARCH_BTN)

    def get_result_title_texts(self):
        """打印搜尋結果標題"""
        self.allure_factory.add_test_step(f"打印搜尋結果標題")
        result_titles = self.get_texts(self.SEARCH_RESULT_TITLE)
        return result_titles
