import os
import chardet
import logging

def ensure_dir(directory):
    """
    確定目錄是否存在，如果不存在則創建它。

    :param directory: 要確定的目錄路徑
    :return: None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f'建立目錄: {directory}')

def detect_encoding(file_path):
    """
    檢測檔案的編碼。

    :param file_path: 要檢測的檔案路徑
    :return: 檔案的編碼（可能為 None）
    :rtype: str or None
    """
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        result = chardet.detect(raw_data)
        logging.debug(f"檔案 {file_path} 的編碼檢測結果：{result['encoding']} (信心度：{result['confidence']})")
        return result['encoding']
    except ImportError as e:
        logging.error(f"ImportError: {e}")
        return None

def read_file(file_path):
    """
    讀取檔案的內容，並嘗試使用適合的編碼讀取。

    1. 首先使用 chardet 庫來檢測檔案的編碼。
    2. 使用上一步驟檢測到的編碼來讀取檔案，並將其內容回傳。

    :param file_path: 要讀取的檔案路徑
    :return: 檔案的內容（可能為 None）
    :rtype: str or None
    """
    detected_encoding = detect_encoding(file_path)
    try:
        with open(file_path, 'r', encoding=detected_encoding) as file:
            content = file.read()
        logging.debug(f'成功讀取 {len(content)} 個字元，使用 {detected_encoding} 編碼')
        return content
    except Exception as e:
        logging.error(f'讀取檔案 {file_path} 時發生錯誤：{e}')
        return None

def write_big5_file(file_path, content):
    """
    將 Big5 編碼的內容寫入到檔案中。

    :param file_path: 要寫入的檔案路徑
    :param content: 要寫入的 Big5 編碼內容（bytes）
    :return: None
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(content)
        logging.debug(f'寫入 {len(content)} 位元組到 {file_path}')
    except Exception as e:
        logging.error(f'寫入檔案 {file_path} 時發生錯誤：{e}')