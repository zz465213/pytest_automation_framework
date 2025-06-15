from datetime import datetime
import platform
import selenium
import requests
import sys

#  ---- 時間常數 ----
START_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")

#  ---- 測試環境資訊 ----
ENV = "local"
TEST_TYPE = "web"
BROWSER = ""
URL = ""
PLATFORM = platform.system() + " " + platform.release()
PYTHON_VERSION = sys.version.split()[0]
SELENIUM_VERSION = selenium.__version__
REQUESTS_VERSION = requests.__version__

#  ---- Driver 設定 ----
# options設定
SANDBOX = "--no-sandbox"
DEV_SHM_USE = "--disable-dev-shm-usage"
GPU_USE = "--disable-gpu"
WINDOW_SIZE = "--window-size=1920,1080"
HEADLESS = False  # 是否啟用無頭模式
# chrome 相關設定
CHROME_LOAD_STRATEGY = "eager"  # Chrome特定頁面加載策略(normal, eager, none)
UNDETECTED_CHROME = False  # 是否啟用防止偵測模式(使用chrome才有用)

#  ---- timeout設定 ----
IMPLICIT_WAIT = 10
TIMEOUT_PAGE_LOAD = 30

#  ---- 截圖設定 ----
ELEMENT_ACTION_SCREENSHOTS = False  # 是否元素執行完動作就截圖，如 False 則只有執行失敗才截圖
ALL_ASSERT_SCREENSHOTS = True  # 是否所有斷言都截圖，如 False 只有斷言失敗才截圖
