import platform
import sys
from datetime import datetime

# ==== 通用設定 ====
# -- 時間常數 --
START_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")
# -- Timeout設定 --
IMPLICIT_WAIT = 10
TIMEOUT_PAGE_LOAD = 30
# -- 截圖設定 --
ELEMENT_ACTION_SCREENSHOTS = False  # 是否元素執行完動作就截圖，如 False 則只有執行失敗才截圖
ALL_ASSERT_SCREENSHOTS = True  # 是否所有斷言都截圖，如 False 只有斷言失敗才截圖

#  ==== 測試環境資訊 ====
ENV = "local"
TEST_TYPE = ""
BROWSER = ""
URL = ""
COMPUTER_PLATFORM = platform.system() + " " + platform.release()
PYTHON_VERSION = sys.version.split()[0]

# ==== Web Driver 設定 ====
# -- Options設定 --
SANDBOX = "--no-sandbox"
DEV_SHM_USE = "--disable-dev-shm-usage"
GPU_USE = "--disable-gpu"
WINDOW_SIZE = "--window-size=1920,1080"
HEADLESS = False  # 是否啟用無頭模式
# -- Chrome 相關設定 --
CHROME_LOAD_STRATEGY = "eager"  # Chrome特定頁面加載策略(normal, eager, none)
UNDETECTED_CHROME = False  # 是否啟用防止偵測模式(使用chrome才有用)
# -- 其他設定 --
HIGH_LIGHT = False  # 如果True，再找到元件時進行高光處理

# ==== App Driver 設定 ====
# -- Options設定 --
REMOTE_URL = "http://localhost:4724"
UUID = ""  # 設備的UUID
APP_PLATFORM = "Android"
APP_PLATFORM_VERSION = "16"
DEVICE_NAME = "emulator-5554"  # 手機裝置名稱(輸入 adb devices 可查)
APP_PACKAGE = "com.android.settings"
APP_ACTIVITY = ".Settings"
LANGUAGE = "en"
LOCALE = "US"
NO_RESET = False  # 是否保留應用程式資料和狀態，False為不保留，則每次執行都為獨立狀態
APP_FILE = ""  # ipa, apk 檔案路徑

