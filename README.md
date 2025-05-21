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
├── config/                  # 設置文件目錄
│   ├── __init__.py
│   ├── config.py            # 基本設置(URL、瀏覽器類型等)
│   └── environment.py       # 環境變數設置
│
├── pages/                   # 頁面對象目錄
│   ├── __init__.py
│   ├── base_page.py         # 基礎頁面類
│   └── login_page.py        # 登入頁面
│
├── test_cases/              # 測試案例目錄
│   ├── __init__.py
│   ├── conftest.py          # Pytest設置和常數設定
│   └── test_login.py        # 登入測試案例
│
├── utils/                   # 工具類目錄
│   ├── __init__.py
│   ├── driver_factory.py    # WebDriver工廠類
│   ├── log_tool.py          # log工具
│   └── wait_tool.py         # 等待輔助工具
│
├── resources/               # 資料文件目錄
│   └── test_datas/          # 測試資料
│
├── reports/                 # 測試報告目錄
│
├── Jenkinsfile              # Jenkins設置文件
├── pytest.ini               # Pytest設置文件
├── requirements.txt         # 專案依賴
└── README.md                # 專案說明
```
