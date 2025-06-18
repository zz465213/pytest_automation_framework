import logging
from pages.base_page import BasePage
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait


class AppBasePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
        self.driver = driver

    def scroll_and_find_element(self, locator, max_scrolls=5):
        locator_str = self._format_locator(locator)
        screen_width = self.driver.get_window_size()["width"]
        screen_height = self.driver.get_window_size()["height"]

        start_x = screen_width * 0.5
        start_y = screen_height * 0.8
        end_y = screen_height * 0.3
        element = None

        for i in range(max_scrolls):
            try:
                element = self.driver.find_element(by=locator[0], value=locator[1])
                break  # 找到元素後跳出迴圈
            except NoSuchElementException:  # 捕獲特定的元素未找到異常
                self.logger.info(f"⚪ 未找到元素，進行向上滑動 (第 {i + 1} 次滑動)")
                self.driver.swipe(start_x, start_y, start_x, end_y, 500)  # 預設滑動持續時間 500ms
            except Exception as e:
                self.logger.error(f"🔴 檢查元素: {locator_str} 或滑動時發生未知錯誤: {e}")
                raise

        if element:
            self.logger.info(f"🟢 成功找到元素：{locator_str} (嘗試次數: {i + 1})")
            return element
        else:
            raise NoSuchElementException(f"🔴 在 {max_scrolls} 次滑動後仍未找到元素：{locator_str}")

    def switch_to_webview_context(self, timeout=5, specific_webview_name=None):
        """
        切換到 Webview 上下文。

        Args:
            timeout (int): 等待 Webview Context 出現的最長時間（秒）
            specific_webview_name (str): 切換到特定名稱的 Webview Context

        Raises:
            WebDriverException: 如果在指定時間內未能找到或切換到 Webview 上下文。
        """
        current_context = self.driver.context
        self.logger.info(f"⚪ 當前 Context: {current_context}")

        try:
            # 等待 Webview Context 出現
            WebDriverWait(self.driver, timeout).until(
                lambda driver: any("WEBVIEW" in c for c in driver.contexts)
            )
            all_contexts = self.driver.contexts
            self.logger.info(f"⚪ 所有可用的 Context: {all_contexts}")

            # 確認 Webview Context 並切換
            if specific_webview_name in all_contexts:
                self.driver.switch_to.context(specific_webview_name)
                self.logger.info(f"🟢 成功切換 Webview Context 到 {specific_webview_name}")
            else:
                self.logger.error(f"🔴 未找到指定 Webview Context = {specific_webview_name}")

        except WebDriverException as e:
            self.logger.error(f"🔴 切換 Webview Context 到 {specific_webview_name} 失敗: {e}")
            raise WebDriverException(f"在 {timeout} 秒內未能切換到 Webview Context。詳細訊息: {e}")
        except Exception as e:
            self.logger.error(f"🔴 切換 Webview Context 到 {specific_webview_name} 時，發生未知錯誤: {e}")
            raise

    def switch_to_native_context(self):
        """
        切換回原生應用上下文 (NATIVE_APP)。
        """
        try:
            self.driver.switch_to.context("NATIVE_APP")
            self.logger.info("🟢 成功切換回原生 Context: NATIVE_APP")
        except Exception as e:
            self.logger.error(f"🔴 切換回原生 Context 失敗: {e}")
            raise
