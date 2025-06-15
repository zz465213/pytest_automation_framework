import logging
import undetected_chromedriver as uc
from configs import global_adapter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class DriverFactory:
    """WebDriver工廠類，負責創建和管理不同類型的WebDriver實例"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _create_options(browser_type):
        """
        創建瀏覽器選項配置

        Args:
            browser_type (str): 瀏覽器類型 (chrome, firefox, edge)

        Returns:
            Options: 瀏覽器選項對象
        """
        options_map = {
            "chrome": webdriver.ChromeOptions(),
            "firefox": webdriver.FirefoxOptions(),
            "edge": webdriver.EdgeOptions()
        }

        options = options_map[browser_type]

        # options選項設定
        options.add_argument(global_adapter.SANDBOX)
        options.add_argument(global_adapter.DEV_SHM_USE)
        options.add_argument(global_adapter.GPU_USE)
        options.add_argument(global_adapter.WINDOW_SIZE)
        if global_adapter.HEADLESS:
            options.add_argument("--headless")

        # Chrome特定配置
        if browser_type == "chrome":
            options.page_load_strategy = global_adapter.CHROME_LOAD_STRATEGY

        return options

    @staticmethod
    def _create_service(browser_type):
        """
        創建瀏覽器服務配置

        Args:
            browser_type (str): 瀏覽器類型 (chrome, firefox, edge)

        Returns:
            Service: 瀏覽器服務對象
        """
        service_map = {
            "chrome": lambda: ChromeService(ChromeDriverManager().install()),
            "firefox": lambda: FirefoxService(GeckoDriverManager().install()),
            "edge": lambda: EdgeService(EdgeChromiumDriverManager().install())
        }

        return service_map[browser_type]()

    @staticmethod
    def _create_driver_instance(browser_type, service, options):
        """
        創建WebDriver實例

        Args:
            browser_type (str): 瀏覽器類型
            service: 瀏覽器服務對象
            options: 瀏覽器選項對象

        Returns:
            WebDriver: WebDriver實例
        """
        driver_map = {
            "chrome": webdriver.Chrome,
            "firefox": webdriver.Firefox,
            "edge": webdriver.Edge,
            "uc": uc.Chrome
        }
        if browser_type not in driver_map:
            raise ValueError(f"不支援的瀏覽器類型: {browser_type}")

        if browser_type == "chrome" and global_adapter.UNDETECTED_CHROME:
            driver = driver_map["uc"]
        else:
            driver = driver_map[browser_type]

        return driver(service=service, options=options)

    def get_driver(self, browser_type):
        """
        根據指定的瀏覽器類型創建WebDriver

        Args:
            browser_type (str): 瀏覽器類型 (chrome, firefox, edge)

        Returns:
            driver: 指定瀏覽器的WebDriver
        """
        browser_type = browser_type.lower()
        self.logger.info(f"⚪ 初始化 {browser_type} WebDriver")

        # 創建各個組件
        options = self._create_options(browser_type)
        service = self._create_service(browser_type)
        driver = self._create_driver_instance(browser_type, service, options)

        return driver
