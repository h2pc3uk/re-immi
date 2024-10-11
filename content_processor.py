import logging

def convert_to_big5(content):
    """
    將 Unicode 字串轉換為 Big5 編碼。

    :param content: 要轉換的 Unicode 字串
    :return: 轉換後的 Big5 編碼字串（bytes），或 None 如果轉換失敗
    :rtype: bytes or None
    """
    try:
        big5_content = content.encode('big5', errors='replace')
        logging.debug(f'轉換為 Big5 編碼，長度：{len(big5_content)} 位元組')
        return big5_content
    except Exception as e:
        logging.error(f'轉換為 Big5 時發生錯誤：{e}')
        return None

def verify_big5_file(file_path):
    """
    驗證檔案是否可以以 Big5 編碼讀取。

    :param file_path: 要驗證的檔案路徑
    :return: None
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read().decode('big5')
        logging.debug(f"成功以 Big5 編碼讀取檔案 {file_path}")
        logging.debug(f"檔案內容預覽：\n{content[:100]}...")  # 只顯示前100個字元
    except UnicodeDecodeError:
        logging.error(f"無法以 Big5 編碼讀取檔案 {file_path}")
    except Exception as e:
        logging.error(f"讀取檔案 {file_path} 時發生錯誤：{e}")

def process_special_file(content, file_type):
    """
    處理特殊的檔案內容，包括：

    1. 移除第一行和最後一行（根據特定條件）
    2. 處理每一行，忽略空行
    3. 將每一行轉換為 Big5 編碼
    4. 確保末尾有一個換行符號

    :param content: 要處理的 Unicode 字串
    :param file_type: 檔案類型（'Fled', 'Immi', 'Punish'）
    :return: 處理後的 Unicode 字串
    :rtype: str
    """
    lines = content.splitlines()

    # 移除第一行和最後一行（根據特定條件）
    if len(lines) > 2:
        if lines[0].startswith('000002!') or lines[0].startswith('084852!'):
            lines = lines[1:]  # 移除第一行
        if lines[-1].startswith('@@'):
            lines = lines[:-1]  # 移除最後一行
    
    processed_lines = []
    for line in lines:
        # 處理每一行，忽略空行
        if not line.strip():
            continue

        parts = line.split('!')
        processed_line = process_line_by_type(parts, file_type)
        if processed_line:
            processed_lines.append(processed_line)
    
    processed_content = '\r\n'.join(processed_lines)
    logging.debug(f'處理 {file_type} 檔案： 移除了首尾行，表留了列對齊，確保末尾有一個換行符號')
    return processed_content

def process_line_by_type(parts, file_type):
    """
    處理每一行，根據檔案類型。

    :param parts: 行內容的分割結果
    :param file_type: 檔案類型（'Fled', 'Immi', 'Punish'）
    :return: 處理後的 Unicode 字串
    :rtype: str
    """
    try:
        if file_type == 'Fled':
            return process_fled_file(parts)
        elif file_type == 'Immi':
            return process_immi_file(parts)
        elif file_type == 'Punish':
            return process_punish_file(parts)
        else:
            logging.error(f'未知的 file_type：{file_type}')
            return None
    except Exception as e:
        logging.error(f'處理行時發生錯誤： {parts}')
        logging.error(f'錯誤詳情： {str(e)}')
        return None

def process_fled_file(parts):
    """
    處理 Fled 檔案的每一行內容。

    :param parts: 行內容的分割結果
    :return: 處理後的 Unicode 字串
    :rtype: str
    """
    result = ['I']
    result.append(parts[1].ljust(10)[:10])
    result.append(parts[2].ljust(50)[:50])
    result.append(parts[3].ljust(15)[:15])
    result.append(parts[4].ljust(3)[:3])
    result.append(parts[5].rjust(8)[:8])
    result.append(parts[6].rjust(1)[:1])
    result.append(parts[7].rjust(8)[:8])
    result.append(parts[8].rjust(8)[:8] if len(parts) > 8 else ' ' * 8)
    result.append(' ' * 7)
    return '!'.join(result)

def process_immi_file(parts):
    """
    處理 Immi 檔案的每一行內容。

    :param parts: 行內容的分割結果
    :return: 處理後的 Unicode 字串
    :rtype: str
    """
    result = ['I' if parts[0] == 'I' else 'U']
    result.append(parts[1].ljust(10)[:10])
    result.append(' ' * 50)
    result.append(parts[3].ljust(15)[:15])
    result.append(parts[4].ljust(3)[:3])
    result.append(parts[5].rjust(8)[:8])
    result.append(parts[6].rjust(1)[:1])
    result.append(parts[7].rjust(8)[:8])
    result.append(parts[8].rjust(1)[:1])
    result.append(' ' * 4)
    return '!'.join(result)

def process_punish_file(parts):
    """
    處理 Punish 檔案的每一行內容。

    :param parts: 行內容的分割結果
    :return: 處理後的 Unicode 字串
    :rtype: str
    """
    result = ['U']
    result.append(parts[1].ljust(10)[:10])
    result.append(' ' * 50)
    result.append(parts[3].ljust(15)[:15])
    result.append(parts[4].ljust(3)[:3])
    result.append(parts[5].rjust(8)[:8])
    result.append(parts[6].rjust(1)[:1])
    result.append(parts[7].rjust(8)[:8])
    result.append(parts[8].rjust(8)[:8])
    result.append(' ' * 7)
    return '!'.join(result)