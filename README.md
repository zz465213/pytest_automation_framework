# 自動化測試框架

## 1. 如何執行
- Web功能性測試: `python run.py --test_type web --browser ** --env ** -m **`
- App功能性測試(測browser): `python run.py --test_type app --browser ** --env ** -m **`
- App功能性測試(調整app package/activity測應用程式): `python run.py --test_type app --env ** -m **`
- Api功能性測試: `python run.py --test_type api --env ** -m **`

## 2. 框架設計理念
- 模組化 (Modularity): 將不同功能的程式碼組織在獨立的模組中，方便管理和維護。
- 可重用性 (Reusability): 透過 fixtures page objects 等方式提高程式碼的重用性。
- 可配置性 (Configurability): 將環境配置、測試數據等外部化，方便在不同環境下執行測試。
- 易讀性 (Readability): 採用清晰的命名規範和程式碼結構，使測試案例易於理解。
- 可擴展性 (Extensibility): 框架設計應考慮未來可能新增的測試類型或工具。

## 3. 框架目錄結構
```
pytest_automation_framework/
│
├── .github/                 # github action CI/CD 使用
│   └── workflows/
│      └── *.yml             # CI/CD 設置文件 
│
├── configs/                 # 設置文件目錄
│   ├── __init__.py
│   ├── common_paths.py      # 共用路徑
│   ├── config.yaml          # 基本設置(URL、使用者資訊等等)
│   └── global_adapter.py    # 全域變數設定
├── logs/                    # 日誌目錄
├── pages/                   # 物件目錄
│   ├── __init__.py              
│   ├── app_base_page.py     # app頁面物件    
│   └── base_page.py         # web頁面物件           
├── reports/                 # 測試報告目錄
├── resources/               # 資料文件目錄
│   ├── payloads/            # api payloads 資料
│   └── test_data/           # 測試資料
├── testcases/               # 測試案例目錄
│   ├── __init__.py
│   └── test_***.py          # 測試案例
├── utils/                   # 共用類目錄
│   ├── __init__.py
│   ├── allure_factory.py    # Allure 工廠類
│   ├── api_factory.py       # API 工廠類
│   ├── driver_factory.py    # WebDriver 工廠類
│   └── file_tool.py         # 文件操作小工具
├── .dockerignore            # Docker 映像建構時排除檔案
├── .gitignore               # Git 版本控制時排除檔案
├── conftest.py              # Pytest設置和常數設定
├── Dockerfile          
├── pytest.ini               # Pytest設置文件
├── README.md 
├── requirements.txt
└── run.py                   # 執行路口
```

## 4. Allure 環境設置:
- 安裝[JDK](<https://www.oracle.com/java/technologies/downloads/>):
  1. 到官網安裝 JDK
  2. JDK 加 $Java_Home 環境變數當中
  3. 環境變數中的 Path 添加 `%Java_Home%/bin`
  4. cmd 輸入 `java -version` 看到版本號表示安裝成功
- 安裝最新版的 [allure-commandline](<https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/>): 
  1. 安裝 allure-commandline.zip
  2. 將 zip 解壓縮
  3. 將 bin 檔加到環境變數當中
  4. cmd 輸入 `allure --version` 看到版本號表示安裝成功

## 5. Appium 環境設置:
- 安裝 JDK 同 `3. Allure 環境設置` 操作
- 安裝 [Android Studio](<https://developer.android.com/studio?hl=zh-tw#get-android-studio/>)
  1. 到官網安裝 Android Studio 的 exe 檔
  2. 本機執行 exe 檔時，在 Select Components to install 勾選 `Android Virtual Device`
  3. SDK(C:\Users\$UserName\AppData\Local\Android\Sdk) 加 $Android_Home 環境變數當中
  4. 環境變數中的 Path 添加 `%Android_Home%\platform-tools` 
  5. 環境變數中的 Path 添加 `%Android_Home%\build-tools`
  6. (舊版本)環境變數中的 Path 添加 `%Android_Home%\tools` or `%Android_Home%\tools\bin` 
  7. (新版本)歡竟變數中的 Path 添加 `%Android_Home%\cmdline-tools\latest\bin`
- 安裝 [Gradle](<https://gradle.org/releases/>)
  1. 到官網選擇一個 binary-only 安裝
  2. 解壓縮後資料夾位置添加到 ` $Gradle_Home ` 環境變數當中
  3. 環境變數中的 Path 添加 ` %Gradle_Home%\bin `
  4. cmd 輸入` gradle --version ` 看到版本號表示安裝成功
- 安裝 [node](<https://nodejs.org/en/download/>)
  1. 到官網選擇 zip 安裝
  2. cmd 輸入` node --version ` 看到版本號表示安裝成功
- 安裝 [Appium Inspector](<https://github.com/appium/appium-inspector/releases/>)
  1. 到 github 選擇一個版本安裝
- 安裝 [Appium GUI](<https://github.com/appium/appium-desktop/releases/>)
  1. 到官網選擇 exe(windows), zip(mac) 安裝
- 安裝 Appium Server
  1. cmd 輸入 `npm i appium@next`
  2. cmd 輸入 `appium --version` 看到版本號表示安裝成功
- 檢查你的 Appium 環境是否已正確配置:
  1. cmd 輸入 `npm i -g appium-doctor` 安裝 Appium Doctor
  2. cmd 輸入 `appium-doctor --version` 看到版本號表示安裝成功
  3. cmd 輸入 `appium-doctor --android`
     - 確認環境(necessary 內條件基本都要完成)
     - 新版本出現error可以不理會: android could NOT be found in C:\Users\USER\AppData\Local\Android\Sdk! 
- 安裝 appium driver 套件:
  1. Appium 用來自動化 Android 裝置上的應用程式: cmd 輸入 `appium driver install uiautomator2`
  2. Appium 控制 Android 上的 Chrome 瀏覽器內容: cmd 輸入 `appium driver install chromium`

## 6. 如何 Build Docker Image
- docker build -t {映像檔名稱}:{映像檔標記} .
- docker run --rm -it -v /$(pwd):/test {映像檔名稱}:{映像檔標記} bash