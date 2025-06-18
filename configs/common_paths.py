import os

# ==== 目錄相關 ====
# -- 根目錄 --
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# -- log相關 --
LOG_DIR = os.path.join(ROOT_DIR, "logs")
# -- 報告相關 --
REPORT_DIR = os.path.join(ROOT_DIR, "reports")
ALLURE_RESULTS_DIR = os.path.join(REPORT_DIR, "allure_results")
ALLURE_REPORT_DIR = os.path.join(REPORT_DIR, "allure_report")
# -- 測案相關 --
TESTCASES_DIR = os.path.join(ROOT_DIR, "testcases")
# -- 資料相關 --
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
PAYLOADS_DIR = os.path.join(RESOURCES_DIR, "payloads")
TEST_DATA_DIR = os.path.join(RESOURCES_DIR, "test_data")
# -- 配置相關 --
CONFIGS_DIR = os.path.join(ROOT_DIR, "configs")
CONFIGS_FILE = os.path.join(CONFIGS_DIR, "configs.yaml")

# ==== 目錄設定 ====
os.makedirs(ROOT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(TESTCASES_DIR, exist_ok=True)
os.makedirs(RESOURCES_DIR, exist_ok=True)
os.makedirs(PAYLOADS_DIR, exist_ok=True)
os.makedirs(TEST_DATA_DIR, exist_ok=True)
os.makedirs(CONFIGS_DIR, exist_ok=True)
