# Pytest 自動化測試框架設計
## 1. 框架設計理念
- 模組化 (Modularity): 將不同功能的程式碼組織在獨立的模組中，方便管理和維護。
- 可重用性 (Reusability): 透過 fixtures page objects 等方式提高程式碼的重用性。
- 可配置性 (Configurability): 將環境配置、測試數據等外部化，方便在不同環境下執行測試。
- 易讀性 (Readability): 採用清晰的命名規範和程式碼結構，使測試案例易於理解。
- 可擴展性 (Extensibility): 框架設計應考慮未來可能新增的測試類型或工具。

## 2. 框架目錄結構
```
pytest_automation_framework/
│
├── allure_requirements/     # 建立 docker image 必要的 allure 壓縮檔目錄
│   ├── allure-2.24.0.tgz
│   └── openjdk-11+28_linux-x64_bin.tar.gz    
│
├── configs/                 # 設置文件目錄
│   ├── __init__.py
│   ├── common_paths.py      # 共用路徑
│   ├── config.yaml          # 基本設置(URL、使用者資訊等等)
│   └── global_adapter.py    # 全域變數設定
│
├── logs/                    # 日誌目錄
│
├── pages/                   # 頁面對象目錄
│   ├── __init__.py
│   ├── base_page.py         # 基礎頁面類
│   └── ***_page.py          # 頁面物件
│
├── reports/                 # 測試報告目錄
│
├── resources/               # 資料文件目錄
│
├── testcases/              # 測試案例目錄
│   ├── __init__.py
│   └── test_***.py          # 測試案例
│
├── utils/                   # 工具類目錄
│   ├── __init__.py
│   ├── allure_factory.py    # Allure Report 工廠類
│   ├── api_factory.py       # API 工廠類
│   ├── driver_factory.py    # WebDriver 工廠類
│   └── file_tool.py         # 文件操作小工具
│
├── .dockerignore            # Docker 映像建構時排除檔案
├── .gitignore               # Git 版本控制時排除檔案
├── conftest.py              # Pytest設置和常數設定
├── Dockerfile          
├── pytest.ini               # Pytest設置文件
├── README.md 
├── requirements.txt
└── run.py                   # 測試路口
```

## 3. 無法產生 Allure Report?
- 安裝[JDK](<https://www.oracle.com/java/technologies/downloads/>):
  1. 到官網安裝JDK
  2. JDK加 $JAVA_HOME 環境變數當中
  3. cmd輸入``` java -version ```看到版本號表示安裝成功
- 安裝最新版的 [allure-commandline](<https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/>): 
  1. 安裝allure-commandline.zip
  2. 將zip解壓縮
  3. 將bin檔加到環境變數當中
  4. cmd輸入``` allure --version ``` 看到版本號表示安裝成功

## 4. 如何 build Docker image
- docker build -t {映像檔名稱}:{映像檔標記} .
- docker run --rm -it -v /$(pwd):/test {映像檔名稱}:{映像檔標記} bash

