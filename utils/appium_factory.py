import logging
from appium import webdriver
from appium.options.common.base import AppiumOptions
from configs import global_adapter


class AppiumFactory:
    """Appium工廠類，負責創建和管理不同平台的App實例"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _create_options(app_platform_type):
        """
        創建瀏覽器選項配置

        Args:
            app_platform_type (str): 平台類型 (android, ios)

        Returns:
            Options: 瀏覽器選項對象
        """
        options = AppiumOptions()
        # options選項設定
        options.set_capability("platformName", global_adapter.APP_PLATFORM)

        if app_platform_type == "android":
            options.set_capability("automationName", "UiAutomator2")
        elif app_platform_type == "ios":
            options.set_capability("automationName", "XCUITest")

        options.set_capability("deviceName", global_adapter.DEVICE_NAME)
        options.set_capability("language", global_adapter.LANGUAGE)
        options.set_capability("locale", global_adapter.LOCALE)
        options.set_capability("noReset", global_adapter.NO_RESET)
        options.set_capability("newCommandTimeout", global_adapter.PAGE_LOAD_WAIT_TIME * 1000)
        options.set_capability("uuid", global_adapter.UUID)
        options.set_capability("app", global_adapter.APP_FILE)
        options.set_capability("appPackage", global_adapter.APP_PACKAGE)
        options.set_capability("appActivity", global_adapter.APP_ACTIVITY)
        if global_adapter.BROWSER.lower() == "chrome":
            # options.set_capability("browserName", "Chrome")
            options.set_capability("appPackage", "com.android.chrome")
            options.set_capability("appActivity", "com.google.android.apps.chrome.Main")
            options.set_capability("chromedriverExecutable",
                                   "C:/Users/USER/Desktop/QA/android_tool/chromedriver-win64/chromedriver.exe")

        return options

    def get_app_driver(self, remote_url, app_platform_type):
        """
        根據指定的平台類型創建AppDriver

        Args:
            remote_url (str): appium 服務器網址
            app_platform_type (str): 平台類型 (android, ios)

        Returns:
            driver: 指定手機平台的AppDriver
        """
        app_platform_type = app_platform_type.lower()
        self.logger.info(f"⚪ 初始化 {app_platform_type} AppDriver")

        # 創建各個組件
        options = self._create_options(app_platform_type)
        driver = webdriver.Remote(remote_url, options=options)

        return driver
