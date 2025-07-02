import allure
import pytest
from pages.app_herokuapp_pages.web.login_page import LoginPage


@allure.epic("HerokuApp登入測試")
@pytest.mark.herokuapp
@pytest.mark.web
class TestWebLogin:
    @allure.feature("正向測試")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.p1
    def test_param_search(self, get_web_driver, get_url, get_username, get_password):
        # Arrange
        login_page = LoginPage(driver=get_web_driver)

        # Action
        login_page.open_page(url=get_url)
        result_title = login_page.user_login(get_username, get_password)

        # Assert
        login_page.assert_equal("Secure Area", result_title)
