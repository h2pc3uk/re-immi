import os
from pathlib import Path
import sys

# 確定專案目錄
def get_project_dir():
    if getattr(sys, 'frozen', False):
        # 如果程式被打包
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

PROJECT_DIR = get_project_dir()
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
DESKTOP_DIR = os.path.join(Path.home(), "Desktop")
MODIFIED_DIR = os.path.join(DESKTOP_DIR, 'modified')