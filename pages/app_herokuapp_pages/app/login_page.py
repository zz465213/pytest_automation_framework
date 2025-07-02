import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.app_base_page import AppBasePage
from utils.appium_factory import AppiumFactory
from utils.allure_factory import AllureFactory


class LoginPage(AppBasePage):
    WITHOUT_ACCT = (AppiumBy.ID, "com.android.chrome:id/signin_fre_dismiss_button")
    GOT_IT_BTN = (AppiumBy.ID, "com.android.chrome:id/ack_button")
    INPUT_SEARCH = (AppiumBy.ID, "com.android.chrome:id/search_box_text")
    HEROKU_SELECTOR = (AppiumBy.ID, "com.android.chrome:id/line_2")
    ENTER_WEB = (AppiumBy.CLASS_NAME, 'android.view.SurfaceView')
    USERNAME_INPUT = (AppiumBy.XPATH, '//*[@id="username"]')
    PASSWORD_INPUT = (AppiumBy.XPATH, '//*[@id="password"]')
    SAVE_PASSWORD_BTN = (AppiumBy.ID, 'com.android.chrome:id/touch_to_fill_button_title')
    CHANGE_PASSWORD_BTN = (AppiumBy.ID, 'com.android.chrome:id/positive_button')
    SECURE_AREA_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Secure Area"]')

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.allure_factory = AllureFactory()
        self.appium_factory = AppiumFactory()
        self.driver = driver

    def enter_heroku_app(self, url):
        """
        1. 開啟 Chrome APP
        2. 關閉[離開帳戶]按鈕
        3. 進入HerokuApp頁面
        """
        self.allure_factory.add_test_step(f"進入HerokuApp主頁")
        self.click_element(self.WITHOUT_ACCT)
        self.click_element(self.GOT_IT_BTN)
        self.input_text(self.INPUT_SEARCH, url)
        self.click_element(self.HEROKU_SELECTOR)

    def user_login(self, username, password):
        """
        1. 輸入帳號密碼進入登入頁
        2. 取得登入首頁標題文字
        """
        self.allure_factory.add_test_step(f"輸入帳號: {username}, 密碼:***")
        self.click_element(self.ENTER_WEB)
        self.switch_to_webview_context(5, "WEBVIEW_chrome")
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        self.switch_to_native_context()
        self.click_element(self.SAVE_PASSWORD_BTN)
        self.click_element(self.CHANGE_PASSWORD_BTN)
        return self.get_text(self.SECURE_AREA_TITLE)
