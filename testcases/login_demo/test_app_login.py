import allure
import os
import pytest
from pages.app_herokuapp_pages.login_page import LoginPage


@allure.epic("HerokuApp登入測試")
@pytest.mark.herokuapp
@pytest.mark.app
class TestAppLogin:

    @allure.feature("正向測試")
    def test_valid_login_heroku_app(self, get_app_driver, get_url, get_username, get_password):
        # Given
        password = os.getenv(get_password)  # 環境變數取出隱碼
        login_page = LoginPage(get_app_driver)
        # When
        login_page.enter_heroku_app(get_url)
        secure_area_title = login_page.user_login(get_username, password)
        # Then
        login_page.assert_equal(secure_area_title, "Secure Area")
