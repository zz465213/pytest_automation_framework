import pytest
import sys
from utils.allure_factory import AllureFactory

# TODO: Jenkins
if __name__ == '__main__':
    # ---- 執行 Pytest ----
    # python run.py --test_type web --browser ** --env ** -m **
    # python run.py --test_type api --env ** -m **
    arg = sys.argv[1:]
    pytest.main(arg)
    # ---- 使用 AllureFactory 產生完整報告 ----
    allure_factory = AllureFactory()
    final_report_path = allure_factory.generate_complete_report()
