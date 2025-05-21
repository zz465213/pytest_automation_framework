# Pytest 自動化測試框架設計
## 1. 框架設計理念
- 模組化 (Modularity): 將不同功能的程式碼組織在獨立的模組中，方便管理和維護。
- 可重用性 (Reusability): 透過 fixtures, helper functions, page objects 等方式提高程式碼的重用性。
- 可配置性 (Configurability): 將環境配置、測試數據等外部化，方便在不同環境下執行測試。
- 易讀性 (Readability): 採用清晰的命名規範和程式碼結構，使測試案例易於理解。
- 可擴展性 (Extensibility): 框架設計應考慮未來可能新增的測試類型或工具。

## 2. 框架目錄結構
```
pytest_automation_framework/
│
├── config/                  # 配置文件目錄
│   ├── __init__.py
│   ├── config.py            # 基本配置(URL、瀏覽器類型等)
│   └── environment.py       # 環境變數配置
│
├── pages/                   # 頁面對象目錄(POM核心)
│   ├── __init__.py
│   ├── base_page.py         # 基礎頁面類
│   ├── login_page.py        # 登入頁面
│   └── dashboard_page.py    # 儀表板頁面
│
├── tests/                   # 測試用例目錄
│   ├── __init__.py
│   ├── conftest.py          # Pytest配置和固件
│   ├── test_login.py        # 登入測試用例
│   └── test_dashboard.py    # 儀表板測試用例
│
├── utils/                   # 工具類目錄
│   ├── __init__.py
│   ├── driver_factory.py    # WebDriver工廠類
│   ├── logger.py            # 日誌工具
│   └── wait_helper.py       # 等待輔助工具
│
├── resources/               # 資源文件目錄
│   ├── test_data/           # 測試數據
│   └── downloads/           # 下載文件
│
├── reports/                 # 測試報告目錄
│   └── allure_results/      # Allure報告數據
│
├── Jenkinsfile              # Jenkins流水線配置
├── pytest.ini               # Pytest配置文件
├── requirements.txt         # 項目依賴
└── README.md                # 項目說明
```
