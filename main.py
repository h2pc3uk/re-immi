import logging
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox
from constants import LOG_DIR, MODIFIED_DIR
from file_utils import ensure_dir, read_file, write_big5_file
from content_processor import convert_to_big5, process_special_file,verify_big5_file
import os

def setup_logging():
    from datetime import datetime
    ensure_dir(LOG_DIR)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f'app_log_{current_time}.txt')
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        encoding='utf-8')

def select_files():
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(title="選擇檔案", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    return files

def process_file(file_path):
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
    for prefix in ['Punish-', 'Fled-', 'Immi-']:
        if prefix in file_name:
            return prefix.rstrip('-')
    return None

def main():
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