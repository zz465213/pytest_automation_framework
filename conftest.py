from configs import global_adapter
import pytest
from utils.allure_factory import AllureFactory
from utils.driver_factory import DriverFactory

allure_factory = AllureFactory()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", choices=["chrome", "firefox", "edge"],
                     help="指定瀏覽器: chrome, firefox, edge")
    parser.addoption("--env", action="store", choices=["ut", "ft", "sit", "uat", "local"],
                     help="指定環境: ut, ft, sit, uat, local")


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
def get_env(request):
    """
    提供環境名稱，如果沒有透過 command line 傳入，則使用 global_adapter.py 中的預設值。
    """
    _env = request.config.getoption("--env")
    if _env:
        global_adapter.ENV = _env
    return global_adapter.ENV


@pytest.fixture(scope="function")
def get_driver(request, get_browser):
    """初始化WebDriver"""
    driver_factory = DriverFactory()
    driver = driver_factory.get_driver(get_browser)
    # driver 設定
    driver.maximize_window()
    driver.set_page_load_timeout(global_adapter.TIMEOUT_PAGE_LOAD)
    driver.implicitly_wait(global_adapter.IMPLICIT_WAIT)

    # 使用 AllureFactory 設定測試標題
    AllureFactory.set_test_title(request.node.name)

    # 提供driver給測試函數
    yield driver

    # 測試結束後關閉瀏覽器
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
def environment_info(get_browser, get_env, get_url):
    """添加測試環境資訊到 Allure 報告"""
    allure_factory.setup_environment_info(get_browser, get_env, get_url)
