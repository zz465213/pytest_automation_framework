import pytest
import sys
import os
from utils.allure_factory import AllureFactory

# TODO: 參考 SeleiumBase 做一個定位
# TODO: Jenkins
if __name__ == '__main__':
    # ---- 執行 Pytest ----
    arg = sys.argv[1:]
    pytest.main(arg)
    # ---- 使用 AllureFactory 產生完整報告 ----
    allure_factory = AllureFactory()
    final_report_path = allure_factory.generate_complete_report()
