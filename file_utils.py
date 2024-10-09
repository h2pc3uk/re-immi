import os
import chardet
import logging

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f'建立目錄: {directory}')

def detect_encoding(file_path):
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
    try:
        with open(file_path, 'wb') as file:
            file.write(content)
        logging.debug(f'寫入 {len(content)} 位元組到 {file_path}')
    except Exception as e:
        logging.error(f'寫入檔案 {file_path} 時發生錯誤：{e}')