import pytest
import sys
from utils.allure_factory import AllureFactory

# TODO: LOG 指令
# TODO: 加入API工廠
# TODO: 添加 TEST_DATA & 參數化測案
# TODO: Jenkins
if __name__ == '__main__':
    # ---- 執行 Pytest ----
    arg = sys.argv[1:]  # python run.py --browser chrome --env local -m yahoo
    pytest.main(arg)
    # ---- 使用 AllureFactory 產生完整報告 ----
    allure_factory = AllureFactory()
    final_report_path = allure_factory.generate_complete_report()
