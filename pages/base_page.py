from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from configs import global_adapter
from utils.allure_factory import AllureFactory
import logging
import time


class BasePage:
    def __init__(self, driver, url):
        self.logger = logging.getLogger(__name__)
        self.driver = driver
        self.url = url
        self.allure_factory = AllureFactory()

    def open_page(self):
        """輸入 URL 開啟頁面"""
        try:
            self.driver.get(self.url)
            self.logger.info(f"🟢 進入頁面: {self.url} 成功")
        except Exception as e:
            self.logger.error(f"🔴 找不到頁面URL: {self.url}, 錯誤訊息: {e}")
            raise

    @staticmethod
    def _format_locator(locator):
        """拆分元素的 by type 跟 locator"""
        by_type, value = locator
        by_type_str = str(by_type).split('.')[-1]  # 提取By類型的名稱部分
        return f"{by_type_str}: {value}"

    def find_element(self, locator):
        """等到可見開始查找單一元素"""
        locator_str = self._format_locator(locator)
        try:
            element = WebDriverWait(self.driver, global_adapter.IMPLICIT_WAIT).until(
                EC.visibility_of_element_located(locator)
            )
            self._highlight_element(element)
            return element
        except Exception as e:
            self.logger.error(f"🔴 找不到元素: {locator_str}, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "element_not_found")
            raise

    def find_elements(self, locator):
        """等到可見開始查找多個元素"""
        locator_str = self._format_locator(locator)
        try:
            elements = WebDriverWait(self.driver, global_adapter.IMPLICIT_WAIT).until(
                EC.visibility_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            self.logger.error(f"🔴 找不到元素: {locator_str}, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "elements_not_found")
            raise

    def click_element(self, locator):
        """等待可見並點擊元素"""
        element = self.find_element(locator)
        locator_str = self._format_locator(locator)
        try:
            element.click()
            self.logger.info(f"🟢 點擊元素: {locator_str}")
            if global_adapter.ELEMENT_ACTION_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "click_passed")
        except Exception as e:
            self.logger.error(f"🔴 點擊元素失敗: {locator_str}, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "click_failed")
            raise

    def input_text(self, locator, text):
        """輸入文字到元素"""
        element = self.find_element(locator)
        locator_str = self._format_locator(locator)
        try:
            element.clear()
            element.send_keys(text)
            self.logger.info(f"🟢 輸入文字【{text}】到元素: {locator_str} 中")
            if global_adapter.ELEMENT_ACTION_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "input_passed")
        except Exception as e:
            self.logger.error(f"🔴 輸入文字【{text}】到元素: {locator_str} 失敗, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "input_failed")
            raise

    def get_text(self, locator):
        """獲取單一元素文字"""
        element = self.find_element(locator)
        locator_str = self._format_locator(locator)
        try:
            self.logger.info(f"🟢 獲取 {locator_str} 元素文字成功")
            if global_adapter.ELEMENT_ACTION_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "get_text_passed")
            return element.text
        except Exception as e:
            self.logger.error(f"🔴 獲取 {locator_str} 元素文字失敗, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "get_text_failed")
            raise

    def get_texts(self, locator):
        """獲取多筆元素文字"""
        elements = self.find_elements(locator)
        locator_str = self._format_locator(locator)
        try:
            texts = [element.text.strip() for element in elements]
            self.logger.info(f"🟢 獲取 {locator_str} 元素文字成功")
            if global_adapter.ELEMENT_ACTION_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "get_text_passed")
            return texts
        except Exception as e:
            self.logger.error(f"🔴 獲取 {locator_str} 元素文字失敗, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "get_text_failed")
            raise

    def is_element_present(self, locator):
        """檢查元素是否存在"""
        locator_str = self._format_locator(locator)
        try:
            WebDriverWait(self.driver, global_adapter.IMPLICIT_WAIT).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"🟢 檢查元素: {locator_str} 存在")
            if global_adapter.ELEMENT_ACTION_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "check_element_passed")
        except Exception as e:
            self.logger.error(f"🔴 檢查元素: {locator_str} 不存在, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "check_element_failed")
            raise

    def action_chain_move_to_element(self, locator):
        """等待可見並點擊元素"""
        element = self.find_element(locator)
        locator_str = self._format_locator(locator)
        try:
            ActionChains(self.driver).move_to_element(element).perform()
            self.logger.info(f"🟢 移動鼠標到元素: {locator_str}")
            if global_adapter.ELEMENT_ACTION_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "move_passed")
        except Exception as e:
            self.logger.error(f"🔴 移動鼠標到元素失敗: {locator_str}, 錯誤訊息: {e}")
            self.allure_factory.take_screenshot(self.driver, "move_failed")
            raise

    def assert_equal(self, expect_result, actual_result):
        """
        斷言預期結果與實際結果是否相等，如斷言發生錯誤進行截圖。
        """
        try:
            assert expect_result == actual_result
            self.logger.info(f"🟢 PASSED - 預期結果: {expect_result}, 實際結果: {actual_result}")
            if global_adapter.ALL_ASSERT_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "assert_passed")
        except AssertionError as e:
            error_msg = f"🔴 FAILED - 預期结果: {expect_result}, 實際結果: {actual_result}, 錯誤訊息: {e}"
            self.logger.error(error_msg)
            self.allure_factory.take_screenshot(self.driver, "assert_failed")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"🔴 FAILED - 斷言過程發生非預期錯誤:{e}, 預期结果: {expect_result}, 實際結果: {actual_result}"
            self.logger.error(error_msg)
            self.allure_factory.take_screenshot(self.driver, "assert_failed")
            raise Exception(error_msg)

    def assert_include(self, expect_result, actual_result):
        """
        斷言預期結果是否包含在實際結果中，如斷言發生錯誤進行截圖。
        """
        try:
            assert expect_result in actual_result
            self.logger.info(f"🟢 PASSED - 預期結果: {expect_result}, 實際結果: {actual_result}")
            if global_adapter.ALL_ASSERT_SCREENSHOTS:
                self.allure_factory.take_screenshot(self.driver, "assert_passed")
        except AssertionError as e:
            error_msg = f"🔴 FAILED - 預期结果: {expect_result}, 實際結果: {actual_result}, 錯誤訊息: {e}"
            self.logger.error(error_msg)
            self.allure_factory.take_screenshot(self.driver, "assert_failed")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"🔴 FAILED - 斷言過程發生非預期錯誤:{e}, 預期结果: {expect_result}, 實際結果: {actual_result}"
            self.logger.error(error_msg)
            self.allure_factory.take_screenshot(self.driver, "assert_failed")
            raise Exception(error_msg)

    def _highlight_element(self, element, blink_speed=0.1):
        """為元素添加邊框顏色閃爍高光效果"""
        try:
            # 先滾動到元素位置
            self.driver.execute_script("""
                arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});
            """, element)

            time.sleep(0.3)

            # 保存原始樣式
            original_style = element.get_attribute("style") or ""

            # Python 控制閃爍順序
            colors = [
                '#ede574', '#f9d423', '#fc913a', 'ff4e50',
                '#ede574', '#f9d423', '#fc913a', 'ff4e50'
            ]

            for i, color in enumerate(colors):
                # 應用當前顏色的邊框
                self.driver.execute_script(
                    f"""
                    var element = arguments[0];
                    var originalStyle = arguments[1];
                    element.style.cssText = originalStyle + 
                    '; border: 3px solid {color} !important;' +
                    '; box-shadow: 0 0 5px {color} !important;' +
                    '; transition: all 0.1s ease !important;';
                    """
                    , element, original_style)

                time.sleep(blink_speed)

            # 恢復原始樣式
            if original_style:
                self.driver.execute_script(
                    "arguments[0].setAttribute('style', arguments[1]);",
                    element, original_style
                )
            else:
                self.driver.execute_script(
                    "arguments[0].removeAttribute('style');",
                    element
                )

        except Exception as e:
            self.logger.warning(f"⚠️ 邊框閃爍高亮元素失敗: {e}")
