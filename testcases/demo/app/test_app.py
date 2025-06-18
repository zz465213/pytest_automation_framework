import allure
import pytest
from pages.herokuapp_pages.login_page import LoginPage


@allure.epic("HerokuApp登入測試")
@pytest.mark.herokuapp
class TestLogin:

    @allure.feature("正向測試")
    def test_valid_login_heroku_app(self, get_app_driver, get_url):
        # Given
        login_page = LoginPage(get_app_driver)
        # When
        login_page.enter_heroku_app(get_url)
        secure_area_title = login_page.user_login("tomsmith", "SuperSecretPassword!")
        # Then
        login_page.assert_equal(secure_area_title, "Secure Area")
