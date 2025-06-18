import allure
import os
import pytest
from configs.common_paths import TEST_DATA_DIR
from pages.yahoo_pages.portal_page import YahooPortalPage
from utils.file_tool import read_data_from_csv


@allure.epic("Yahoo搜尋測試")
@allure.feature("搜尋飯店")
@pytest.mark.yahoo
@pytest.mark.web
class TestYahooPortal:
    @allure.story("測試參數化輸入，正向搜尋飯店且驗證飯店所在縣市是否包含在標題內")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "search_input, expect_result",
        [
            ("台南飯店", "台南"),
            ("台中飯店", "台中"),
            ("台北飯店", "台北")
        ]
    )
    def test_param_search(self, get_web_driver, get_url, search_input, expect_result):
        # Arrange
        login_page = YahooPortalPage(driver=get_web_driver)

        # Action
        login_page.open_page(url=get_url)
        login_page.search_result(search_input)

        # Assert
        for actual_result in login_page.get_result_title_texts():
            login_page.assert_include(expect_result, actual_result)

    @allure.story("測試參數化輸入，正向搜尋飯店且驗證飯店所在縣市是否包含在標題內")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.csv
    @pytest.mark.parametrize(
        "search_input, expect_result",
        read_data_from_csv(os.path.join(TEST_DATA_DIR, "hotel_data.csv"))
    )
    def test_csv_param_search(self, get_web_driver, get_url, search_input, expect_result):
        # Arrange
        login_page = YahooPortalPage(driver=get_web_driver)

        # Action
        login_page.open_page(url=get_url)
        login_page.search_result(search_input)

        # Assert
        for actual_result in login_page.get_result_title_texts():
            login_page.assert_include(expect_result, actual_result)

    @allure.story("正向測試，搜尋飯店且驗證飯店所在縣市是否包含在標題內")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.success
    def test_valid_search(self, get_web_driver, get_url):
        # Arrange
        login_page = YahooPortalPage(driver=get_web_driver)

        # Action
        login_page.open_page(url=get_url)
        login_page.search_result("台北飯店")

        # Assert
        for actual_result in login_page.get_result_title_texts():
            login_page.assert_include("台北", actual_result)

    @allure.story("反向測試，搜尋飯店且錯誤驗證飯店所在縣市是否包含在標題內")
    @allure.severity(allure.severity_level.TRIVIAL)
    @pytest.mark.fail
    def test_fail_search(self, get_web_driver, get_url):
        # Arrange
        login_page = YahooPortalPage(driver=get_web_driver)

        # Action
        login_page.open_page(url=get_url)
        login_page.search_result("台南飯店")

        # Assert
        for actual_result in login_page.get_result_title_texts():
            login_page.assert_include("台中", actual_result)
