import allure
import json
import logging
import requests
import selenium
import importlib.metadata
import glob
from configs import global_adapter
from configs.common_paths import *
from datetime import datetime
from utils import file_tool, img_tool


class AllureFactory:
    @staticmethod
    def _generate_allure_report():
        """
        生成 Allure HTML 報告
        """
        allure_command = f"allure generate {ALLURE_RESULTS_DIR} -o {ALLURE_REPORT_DIR} --clean"
        exit_code = os.system(allure_command)

        if exit_code == 0:
            logging.info(f"🟢 Allure HTML 報告成功產生於: {ALLURE_REPORT_DIR}")
        else:
            logging.error("🔴 Allure HTML 報告產生失敗")
            raise Exception

    @staticmethod
    def _compress_and_cleanup_images():
        """
        壓縮報告內 JPG/JPEG 圖片，並轉換為 WEBP 格式。
        """
        attachments_dir = f"{ALLURE_REPORT_DIR}/data/attachments"
        try:
            # 取得jpg截圖
            jpg_files_path = glob.glob(os.path.join(attachments_dir, "*.jpg")) + \
                             glob.glob(os.path.join(attachments_dir, "*.jpeg"))
            # 舊檔案壓縮成webp並移除
            for jpg_file_path in jpg_files_path:
                img_tool.compress_image(input_path=jpg_file_path, output_path=jpg_file_path,
                                        img_quality=30, img_format="WEBP")
            logging.info(f"🟢 壓縮報告圖片成功")
        except Exception as e:
            logging.error(f"🔴 壓縮路徑:[{attachments_dir}] 的報告圖片失敗，失敗訊息: {e}")
            raise Exception

    @staticmethod
    def _combine_allure_report():
        """
        合併 Allure 報告為單一 HTML 文件
        """
        combine_command = f"allure-combine {ALLURE_REPORT_DIR} --dest {REPORT_DIR}"
        combine_exit_code = os.system(combine_command)
        if combine_exit_code == 0:
            logging.info(f"🟢 合併報告成功，並產生於: {REPORT_DIR}")
        else:
            logging.error("🔴 合併報告失敗")
            raise Exception

    def generate_report_flow(self):
        """
        完整的報告生成流程

        Returns:
            str: 最終報告文件路徑，失敗返回舊路徑
        """
        report_filename = f"report_{global_adapter.START_TIME}.html"
        old_report_path = f"{REPORT_DIR}/complete.html"
        new_report_path = f"{REPORT_DIR}/{report_filename}"

        self._generate_allure_report()
        self._compress_and_cleanup_images()
        self._combine_allure_report()

        file_tool.cleanup_folder(ALLURE_RESULTS_DIR)
        file_tool.cleanup_folder(ALLURE_REPORT_DIR)
        final_report_path = file_tool.rename_file(old_report_path, new_report_path)
        return final_report_path

    @staticmethod
    def _get_selenium_environment_data(env, test_type, browser, url):
        """
        產生 Web 測試環境資訊

        Args:
            env (str): 環境名稱
            test_type(str): 測試類型
            browser (str): 瀏覽器名稱
            url (str): 測試 URL

        Returns:
            dict: Web測試環境資訊
        """
        env_data = {
            "TestType": test_type.capitalize(),
            "Environment": env.capitalize(),
            "Platform": global_adapter.COMPUTER_PLATFORM,
            "PythonVersion": global_adapter.PYTHON_VERSION,
            "Browser": browser.capitalize(),
            "SeleniumVersion": selenium.__version__,
            "URL": url
        }
        return env_data

    @staticmethod
    def _get_request_environment_data(env, test_type):
        """
        產生 Api 測試環境資訊

        Args:
            env (str): 環境名稱
            test_type(str): 測試類型

        Returns:
            dict: Api測試環境資訊
        """
        env_data = {
            "TestType": test_type.upper(),
            "Environment": env.capitalize(),
            "Platform": global_adapter.COMPUTER_PLATFORM,
            "PythonVersion": global_adapter.PYTHON_VERSION,
            "RequestsVersion": requests.__version__
        }
        return env_data

    @staticmethod
    def _get_appium_environment_data(env, test_type, browser, url):
        """
        產生 App 測試環境資訊

        Args:
            env (str): 環境名稱
            test_type(str): 測試類型
            browser (str): 瀏覽器名稱
            url (str): 測試 URL

        Returns:
            dict: App測試環境資訊
        """
        env_data = {
            "TestType": test_type.upper(),
            "Environment": env.capitalize(),
            "Platform": global_adapter.COMPUTER_PLATFORM,
            "PythonVersion": global_adapter.PYTHON_VERSION,
            "AppiumVersion": importlib.metadata.version("Appium-Python-Client"),
            "AppVersion": f"{global_adapter.APP_PLATFORM} {global_adapter.APP_PLATFORM_VERSION}"
        }

        if browser:
            env_data["Browser"] = browser
            env_data["URL"] = url
        return env_data

    def setup_environment_info(self, env, test_type, browser, url):
        """
        設定測試環境資訊到 Allure 報告。

        Args:
            env (str): 環境名稱
            test_type(str): 測試類型
            browser (str): 瀏覽器名稱
            url (str): 測試 URL
        """
        # 獲取測試環境資訊
        if test_type.lower() == "web":
            env_data = self._get_selenium_environment_data(env, test_type, browser, url)
        elif test_type.lower() == "app":
            env_data = self._get_appium_environment_data(env, test_type, browser, url)
        elif test_type.lower() == "api":
            env_data = self._get_request_environment_data(env, test_type)
        else:
            raise ValueError(f"🔴 輸入錯誤的 TestType = {test_type}")

        # 確保 Allure 結果目錄存在
        os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

        # 將測試環境資訊寫入 environment.properties 文件
        env_file_path = os.path.join(ALLURE_RESULTS_DIR, "environment.properties")
        env_data_content = "\n".join(f"{key}={value}" for key, value in env_data.items()) + "\n"
        file_tool.write_file(env_file_path, env_data_content)

        # environment.properties 添加到 Allure 報告中
        allure.attach(
            json.dumps(env_data, indent=4, ensure_ascii=False),
            name="environment_info",
            attachment_type=allure.attachment_type.JSON
        )

    def capture_failure_screenshot(self, driver, case_name=None):
        """
        捕獲失敗時的截圖和頁面源碼

        Args:
            driver: WebDriver 實體
            case_name (str, optional): 測試名稱
        """
        if not driver:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"failure_{timestamp}"
        if case_name:
            screenshot_name = f"failure_{case_name}_{timestamp}"
        self.take_screenshot(driver, screenshot_name)

    @staticmethod
    def set_test_title(test_name):
        """
        設定測試標題

        Args:
            test_name (str): 測試名稱
        """
        allure.dynamic.title(test_name)

    @staticmethod
    def add_test_step(step_name):
        """
        添加測試步驟

        Args:
            step_name (str): 步驟名稱
        """
        with allure.step(step_name):
            pass

    @staticmethod
    def attach_text(content, name, attachment_type=allure.attachment_type.TEXT):
        """
        附加文本內容到報告

        Args:
            content (str): 內容
            name (str): 附件名稱
            attachment_type: 附件類型
        """
        allure.attach(content, name=name, attachment_type=attachment_type)

    @staticmethod
    def attach_file(file_path, name=None):
        """
        附加文件到報告

        Args:
            file_path (str): 文件路徑
            name (str, optional): 附件名稱
        """
        if not name:
            name = os.path.basename(file_path)
        allure.attach.file(file_path, name=name)

    @staticmethod
    def take_screenshot(driver, name="screenshot"):
        """截圖並添加到 Allure Report 當中"""
        allure.attach(
            driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.JPG
        )
