import logging
import os
import pytest
from configs import global_adapter
from configs.common_paths import LOG_DIR
from datetime import datetime
from utils.allure_factory import AllureFactory
from utils.appium_factory import AppiumFactory
from utils.driver_factory import DriverFactory


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"test_run_{timestamp}.log"
    log_file_path = os.path.join(LOG_DIR, log_file_name)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )
    yield


def pytest_configure(config):
    """
    在 pytest 運行之前配置日誌文件路徑
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"test_run_{timestamp}.log"
    log_file_path = os.path.join(LOG_DIR, log_file_name)

    # 將日誌文件路徑設定給 pytest 的配置，這樣 pytest 內部的日誌處理會使用這個文件
    config.option.log_file = log_file_path
    config.option.log_file_level = "INFO"
    config.option.log_file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    config.option.log_file_date_format = "%Y%m%d_%H%M%S"

    # 設置根 logger 的級別，確保所有級別的日誌都能被捕獲
    logging.getLogger().setLevel(logging.INFO)


def pytest_addoption(parser):
    parser.addoption("--test_type", action="store", choices=["api", "web", "app"],
                     help="指定測試類型: api, web, app")
    parser.addoption("--browser", action="store", choices=["chrome", "firefox", "edge"],
                     help="指定瀏覽器: chrome, firefox, edge")
    parser.addoption("--env", action="store", choices=["ut", "sit", "uat", "local"],
                     help="指定環境: ut, sit, uat, local")


@pytest.fixture(scope="session")
def get_env(request):
    """
    提供環境名稱，如果沒有透過 command line 傳入，則使用 global_adapter.py 中的預設值。
    """
    _env = request.config.getoption("--env")
    if _env:
        global_adapter.ENV = _env
    return global_adapter.ENV


@pytest.fixture(scope="session")
def get_test_type(request):
    """
    提供測試類型，如果沒有透過 command line 傳入，則使用 global_adapter.py 中的預設值。
    """
    _test_type = request.config.getoption("--test_type")
    if _test_type:
        global_adapter.TEST_TYPE = _test_type
    return global_adapter.TEST_TYPE


@pytest.fixture(scope="session")
def get_browser(request):
    """
    提供瀏覽器名稱，如果沒有透過 command line 傳入，則使用 global_adapter.py 中的預設值。
    """
    _browser = request.config.getoption("--browser")
    if _browser:
        global_adapter.BROWSER = _browser
    return global_adapter.BROWSER


@pytest.fixture(scope="session")
def get_url(request):
    """
    提供 global_adapter.py 中預設的 URL (從 Conftest 帶入使用)
    """
    return global_adapter.URL


@pytest.fixture(scope="function")
def get_web_driver(request, get_browser):
    """初始化WebDriver"""
    driver_factory = DriverFactory()
    driver = driver_factory.get_web_driver(get_browser)

    # driver 設定
    driver.maximize_window()
    driver.set_page_load_timeout(global_adapter.TIMEOUT_PAGE_LOAD)
    driver.implicitly_wait(global_adapter.IMPLICIT_WAIT)

    AllureFactory.set_test_title(request.node.name)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def get_app_driver(request, get_browser):
    """初始化AppDriver"""
    appium_factory = AppiumFactory()

    # 選擇 Appium 測試裝置(uuid未填則用虛擬機)
    app_device = global_adapter.REMOTE_URL
    if global_adapter.UUID:
        app_device = global_adapter.UUID
    driver = appium_factory.get_app_driver(app_device, global_adapter.APP_PLATFORM)

    AllureFactory.set_test_title(request.node.name)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """在測試失敗時捕獲截圖"""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver")
    if not driver:
        return

    AllureFactory.capture_failure_screenshot(driver, item.name)


@pytest.fixture(scope="session", autouse=True)
def environment_info(get_env, get_test_type, get_browser, get_url):
    """添加測試環境資訊到 Allure 報告"""
    allure_factory = AllureFactory()
    allure_factory.setup_environment_info(get_env, get_test_type, get_browser, get_url)
