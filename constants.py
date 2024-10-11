import os
from pathlib import Path
import sys

# 確定專案目錄
def get_project_dir():
    """
    返回專案目錄的路徑。

    如果腳本是直接執行的，使用 os.path.abspath(__file__) 來取得 Python 腳本的路徑。
    如果腳本是由 pyinstaller 產生的可執行檔執行的，則使用 os.path.dirname(sys.executable)。

    回傳：
    str：專案目錄的路徑。
    """
    if getattr(sys, 'frozen', False):
        # 如果程式被打包
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = get_project_dir()
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
DESKTOP_DIR = os.path.join(Path.home(), "Desktop")
MODIFIED_DIR = os.path.join(DESKTOP_DIR, 'modified')