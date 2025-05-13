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
├── tests/                      # 測試案例目錄
│   ├── api/                    # API 測試案例
│   │   └── test_***.py
│   ├── web_selenium/           # Selenium Web UI 測試案例
│   │   └── test_***.py
│   ├── web_playwright/         # Playwright Web UI 測試案例
│   │   └── test_***.py
│   └── mobile_appium/          # Appium Mobile App 測試案例
│       └── test_***.py
├── framework/                  # 框架核心程式碼
│   ├── base/                   # 基礎類別和輔助函式
│   │   ├── api_base.py         # API 請求基礎類別
│   │   ├── web_base_selenium.py # Selenium Web UI 測試基礎頁面/操作類別
│   │   ├── web_base_playwright.py # Playwright Web UI 測試基礎頁面/操作類別
│   │   └── mobile_base_appium.py # Appium Mobile App 測試基礎頁面/操作類別
│   ├── utils/                  # 通用工具模組
│   │   ├── config_manager.py   # 設定檔讀取與管理
│   │   ├── logger.py           # 日誌記錄
│   │   └── reporting_utils.py  # 報告相關輔助 (例如：截圖)
│   ├── pages/                  # Page Object Model (POM) 相關頁面物件
│   │   ├── web_selenium_pages/
│   │   │   └── login_page_selenium.py
│   │   ├── web_playwright_pages/
│   │   │   └── home_page_playwright.py
│   │   └── mobile_appium_pages/
│   │       └── welcome_page_appium.py
│   └── drivers/                # WebDriver 和 Appium Driver 管理
│       ├── browser_factory_selenium.py  # Selenium 瀏覽器驅動工廠
│       ├── browser_factory_playwright.py # Playwright 瀏覽器實例管理
│       └── appium_driver_manager.py    # Appium 驅動管理
├── config/                     # 設定檔目錄
│   ├── config.ini              # 主要設定檔 (或 .yaml, .json)
│   ├── environments/           # 環境特定設定檔
│   │   ├── dev.ini
│   │   └── staging.ini
│   └── test_data/              # 測試數據 (可為 .json, .csv, .yaml 等)
│       └── users.json
├── reports/                    # 測試報告存放目錄 (e.g., Allure reports)
├── logs/                       # 日誌檔案存放目錄
├── conftest.py                 # Pytest 的本地 plugin，定義全局 fixtures
├── requirements.txt            # 專案依賴套件
└── README.md                   # 專案說明文件
```
