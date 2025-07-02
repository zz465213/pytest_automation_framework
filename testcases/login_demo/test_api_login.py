import allure
import pytest
from utils.api_factory import APIFactory
from bs4 import BeautifulSoup


@allure.epic("HerokuApp登入測試")
@pytest.mark.herokuapp
@pytest.mark.api
class TestApiLogin:

    @allure.feature("正向測試")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.p1
    def test_valid_login(self, get_json):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = get_json["body"]["username"]
        password = get_json["body"]["password"]
        body = f"username={username}&password={password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("You logged into a secure area!", result)

    @allure.feature("反向測試: 空值帳號")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p2
    def test_empty_username_login(self, get_json):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = ""
        password = get_json["body"]["password"]
        body = f"username={username}&password={password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("Your username is invalid!", result)

    @allure.feature("反向測試: 錯誤帳號")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p2
    def test_invalid_username_login(self, get_json):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = get_json["body"]["username"]
        password = get_json["body"]["password"]
        body = f"username=x{username}&password={password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("Your username is invalid!", result)

    @allure.feature("反向測試: 空值密碼")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p2
    def test_empty_password_login(self, get_json):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = get_json["body"]["username"]
        password = ""
        body = f"username={username}&password={password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("Your password is invalid!", result)

    @allure.feature("反向測試: 錯誤密碼")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.p2
    def test_invalid_password_login(self, get_json):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = get_json["body"]["username"]
        password = get_json["body"]["password"]
        body = f"username={username}&password=X{password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("Your password is invalid!", result)

    @allure.feature("反向測試: 錯誤帳號及密碼")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p3
    def test_invalid_password_login(self, get_json):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = get_json["body"]["username"]
        password = get_json["body"]["password"]
        body = f"username=X{username}&password=X{password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("Your username is invalid!", result)

    @pytest.mark.parametrize("symbol",
                             [("!"), ("@"), ("#"), ("$"), ("%"), ("^"), ("&"), ("*"), ("("), (")"), ("_"), ("+"), ("-"),
                              ("="), ("["), ("]"), ("\\"), ("{"), ("}"), ("|"), (";"), (":"), ("'"), ("`"), (","),
                              ("."), ("/"), ("<"), (">"), ("?"), ("~"), ("\"")])
    @allure.feature("反向測試: 錯誤符號帳號")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p3
    def test_invalid_symbol_username_login(self, get_json, symbol):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = get_json["body"]["username"]
        password = get_json["body"]["password"]
        body = f"username={symbol}{username}&password={password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("Your username is invalid!", result)

    @pytest.mark.parametrize("symbol",
                             [("!"), ("@"), ("#"), ("$"), ("%"), ("^"), ("&"), ("*"), ("("), (")"), ("_"), ("+"), ("-"),
                              ("="), ("["), ("]"), ("\\"), ("{"), ("}"), ("|"), (";"), (":"), ("'"), ("`"), (","),
                              ("."), ("/"), ("<"), (">"), ("?"), ("~"), ("\"")])
    @allure.feature("反向測試: 錯誤符號密碼")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.p3
    def test_invalid_symbol_password_login(self, get_json, symbol):
        # Given
        header = get_json["header"]
        header["Upgrade-Insecure-Requests"] = "1"
        username = get_json["body"]["username"]
        password = get_json["body"]["password"]
        body = f"username={username}&password={symbol}{password}"
        heroku_app_api = APIFactory("https://the-internet.herokuapp.com")

        # When
        heroku_app_api.get_text("/login")
        res_context = heroku_app_api.post_text(endpoint="/authenticate", headers=header, data=body)
        res_context = BeautifulSoup(res_context, 'html.parser')
        result = res_context.find('div', id='flash')
        result = result.get_text(strip=True)[:-1]

        # Then
        heroku_app_api.assert_equal("Your password is invalid!", result)
