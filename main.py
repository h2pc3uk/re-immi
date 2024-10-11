import logging
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
from constants import LOG_DIR, MODIFIED_DIR
from file_utils import ensure_dir, read_file, write_big5_file
from content_processor import convert_to_big5, process_special_file,verify_big5_file
import os

def setup_logging():
    """
    配置 logging 模組將除錯級別的日誌寫入到名為 "app_log_<當前日期和時間>.txt" 的檔案中，該檔案位於 LOG_DIR 目錄。
    日誌檔案使用 UTF-8 編碼，格式為：
    "%(asctime)s - %(levelname)s - %(message)s"。
    """
    from datetime import datetime
    ensure_dir(LOG_DIR)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f'app_log_{current_time}.txt')
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        encoding='utf-8')

def select_files():
    """
    打開檔案對話框以選取多個檔案。

    對話框預設顯示 *.txt 檔案，但允許選取所有類型的檔案。該函式返回使用者選取的檔案路徑的元組。
    如果未選取任何檔案，則返回空元組。

    :return: 檔案路徑的元組。
    :rtype: tuple
    """
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(title="選擇檔案", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return files

def process_file(file_path):
    """
    處理檔案，通過讀取其內容，根據其類型（由檔案名稱判定）進行處理，將其轉換為 Big5 編碼，並寫入到 MODIFIED_DIR 目錄中的新檔案，並驗證輸出檔案可以使用 Big5 編碼讀取。

    如果檔案類型未知，會記錄一則警告，並返回 None。
    如果處理的任何步驟失敗，會記錄一則錯誤，並返回 None。

    :param file_path: 要處理的檔案路徑。
    :return: 已處理檔案的路徑，或在發生錯誤時返回 None。
    :rtype: str 或 None
    """
    content = read_file(file_path)
    if content is None:
        return None

    file_name = os.path.basename(file_path)
    file_type = get_file_type(file_name)

    # 根據檔名判斷檔案類型並處理
    if file_type:
        if file_type == 'Immi':
            content = content.replace('|', '!')

        content = process_special_file(content, file_type)
        if content is None:
            logging.error(f'處理 {file_type} 檔案時發生錯誤')
            return None
    else:
        logging.warning(f'未知的檔案類型：{file_name}')

    big5_content = convert_to_big5(content)
    if big5_content is None:
        return None
    
    output_path = os.path.join(MODIFIED_DIR, file_name)
    write_big5_file(output_path, big5_content)
    verify_big5_file(output_path)
    return output_path

def get_file_type(file_name):
    """
    從檔案名稱中獲取檔案類型（“Punish”、“Fled” 或 “Immi” 其中之一）。

    該函式通過遍歷可能的前綴，並檢查檔案名稱是否包含該前綴來運作。
    如果找到匹配，則返回去除尾部 ‘-’ 的前綴。如果未找到匹配，則返回 None。

    :param file_name: 要判定類型的檔案名稱。
    :return: 檔案的類型，或在類型未知時返回 None。
    :rtype: str 或 None
    """
    for prefix in ['Punish-', 'Fled-', 'Immi-']:
        if prefix in file_name:
            return prefix.rstrip('-')
    return None

def main():
    """
    處理命令列參數與檔案選取對話框。

    該函式處理以下步驟：

	1.	檢查 MODIFIED_DIR 目錄是否存在，如果不存在則創建它。
	2.	使用 argparse 解析命令列參數。
	3.	如果沒有指定檔案，則打開檔案對話框以選取多個檔案。
	4.	透過呼叫 process_file 來處理每個檔案，該函式會讀取檔案內容，根據其類型（由檔案名稱判定）進行處理，將其轉換為 Big5 編碼，並寫入到 MODIFIED_DIR 目錄中的新檔案，並驗證輸出檔案可以使用 Big5 編碼讀取。
	5.	顯示一個包含處理結果的訊息框，包括成功與失敗轉換的數量。
    """
    
    ensure_dir(MODIFIED_DIR)
    parser = argparse.ArgumentParser(description='將檔案轉換為 Big5 編碼。')
    parser.add_argument('files', nargs='*', help='要轉換的輸入檔案')
    args = parser.parse_args()

    if not args.files:
        args.files = select_files()

    if not args.files:
        messagebox.showinfo("提示", "沒有選擇任何檔案，程式結束。")
        return

    success_count = 0
    fail_count = 0
    for file in args.files:
        if not os.path.exists(file):
            logging.error(f'錯誤：檔案 {file} 不存在')
            fail_count += 1
            continue

        output_file = process_file(file)
        if output_file:
            logging.info(f'成功將 {file} 轉換為 {output_file}')
            success_count += 1
        else:
            logging.error(f'轉換 {file} 失敗')
            fail_count += 1
        logging.debug('-' * 50)
    messagebox.showinfo("處理結果", f"處理完成！\n成功轉換： {success_count} 份檔案\n失敗轉換： {fail_count} 份檔案\n\n轉換後的檔案位於：\n{MODIFIED_DIR}。")

if __name__ == "__main__":
    setup_logging()
    try:
        main()
    except Exception as e:
        logging.exception("程式執行時發生錯誤")
        messagebox.showerror("錯誤", f"程式執行時發生錯誤：\n{str(e)}")
    finally:
        logging.debug("程式結束執行")