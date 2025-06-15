import allure
import json
import logging
from configs import global_adapter
from configs.common_paths import *
from datetime import datetime
from utils import file_tool


class AllureFactory:
    @staticmethod
    def generate_allure_report():
        """
        生成 Allure HTML 報告

        Returns:
            bool: 成功返回 True，失敗返回 False
        """
        allure_command = f"allure generate {ALLURE_RESULTS_DIR} -o {ALLURE_REPORT_DIR} --clean"

        exit_code = os.system(allure_command)

        if exit_code == 0:
            logging.info(f"🟢 Allure HTML 報告成功產生於: {ALLURE_REPORT_DIR}")
        else:
            logging.error("🔴 Allure HTML 報告產生失敗")
            raise Exception

    @staticmethod
    def combine_allure_report():
        """
        合併 Allure 報告為單一 HTML 文件

        Returns:
            bool: 成功返回 True，失敗返回 False
        """
        combine_command = f"allure-combine {ALLURE_REPORT_DIR} --dest {REPORT_DIR}"
        combine_exit_code = os.system(combine_command)
        if combine_exit_code == 0:
            logging.info(f"🟢 合併報告成功，並產生於: {REPORT_DIR}")
        else:
            logging.error("🔴 合併報告失敗")
            raise Exception

    def generate_complete_report(self):
        """
        完整的報告生成流程

        Returns:
            str: 最終報告文件路徑，失敗返回舊路徑
        """
        report_filename = f"report_{global_adapter.START_TIME}.html"
        old_path = f"{REPORT_DIR}/complete.html"
        new_path = f"{REPORT_DIR}/{report_filename}"

        self.generate_allure_report()
        self.combine_allure_report()
        file_tool.cleanup_folder(ALLURE_RESULTS_DIR)
        file_tool.cleanup_folder(ALLURE_REPORT_DIR)
        final_report_path = file_tool.rename_file(old_path, new_path)
        return final_report_path

    @staticmethod
    def get_selenium_environment_data(env, test_type, browser, url):
        """
        產生測試環境資訊的字典。

        Args:
            env (str): 環境名稱
            test_type(str): 測試類型
            browser (str): 瀏覽器名稱
            url (str): 測試 URL

        Returns:
            dict: 包含測試環境資訊的字典
        """
        env_data = {
            "TestType": test_type.upper(),
            "Environment": env.capitalize(),
            "Platform": global_adapter.PLATFORM,
            "PythonVersion": global_adapter.PYTHON_VERSION,
        }

        if test_type in ["web", "app"]:
            env_data["Browser"] = browser
            env_data["URL"] = url
        if test_type == "web":
            env_data["SeleniumVersion"] = global_adapter.SELENIUM_VERSION
        elif test_type == "api":
            env_data["RequestsVersion"] = global_adapter.REQUESTS_VERSION
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
        # 從獨立函數獲取環境數據
        env_data = self.get_selenium_environment_data(env, test_type, browser, url)

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
