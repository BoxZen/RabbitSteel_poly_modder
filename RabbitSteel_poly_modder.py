import csv
import locale


def get_system_language() -> str:
    """
    偵測系統語言，返回 'zh' (中文) 或 'en' (英文)\n
    Detects the system language and returns 'zh' (Chinese) or 'en' (English)
    """
    try:
        # 取得系統預設語系（例如 zh_TW, zh_CN, en_US）
        lang, _ = locale.getlocale()
        if lang and lang.startswith('Chinese'):
            return 'zh'
    except:
        pass
    return 'en'

def merge_name_to_description(names_path, desc_path, output_path, source_lang="English", target_lang="Chinese") -> None:
    """
    將 names_path 的指定語言(source_lang) 物品名，
    複製到 desc_path 的指定語言(target_lang) 前方，並加上 # 符號。\n
    copy source_lang in names_path to target_lang in desc_path, and add # symbol.
    """

    # 1. 讀取 Names_Item.csv，建立 key -> 物品名稱 的映射表
    name_lookup = {}
    with open(names_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row.get('key')
            if key:
                name_lookup[key] = row.get(source_lang, '')

    # 2. 讀取 Descriptions_Item.csv 並進行內容修改
    updated_rows = []
    fieldnames = []
    
    with open(desc_path, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            key = row.get('key')
            if key in name_lookup and target_lang in row:
                item_name = name_lookup[key]
                original_desc = row[target_lang]
                
                # [名稱]#[說明]
                row[target_lang] = f"{item_name}#{original_desc}"
                
            updated_rows.append(row)

    # 3. 將結果寫入新的 CSV 檔案（或覆蓋原檔）
    with open(output_path, mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
        
    msg = f"完成！已建立檔案: {output_path}" if sys_lang == 'zh' else f"Done! Created file: {output_path}"
    print(msg)

def language_selection() -> str:
    """
    提供語言選擇功能，返回對應的語言名稱。
    """
    lang_map = {
        1: "English",
        2: "Japanese",
        3: "Chinese",
        4: "Korean",
        5: "Ukrainian",
        6: "French"
    }
    
    while True:
        try:
            choice = int(input("(1: English, 2: Japanese, 3: Chinese, 4: Korean, 5: Ukrainian, 6: French): "))
            if choice in lang_map:
                return lang_map[choice]
            else:
                msg = "無效的選擇，請再試一次。" if sys_lang == 'zh' else "Invalid choice, please try again."
                print(msg)
        except ValueError:
            msg = "請輸入有效的數字。" if sys_lang == 'zh' else "Please enter a valid number."
            print(msg)


if __name__ == "__main__":
    NAMES_FILE = "./Data/Names_Item.csv"
    DESC_FILE = "./Data/Descriptions_Item.csv"
    OUTPUT_FILE = "Descriptions_Item.csv"
    sys_lang = get_system_language()

    msg = "請選擇次要語言" if sys_lang == 'zh' else "Select the Sub Language "
    print(msg)
    SOURCE_LANG = language_selection()
    msg = "請選擇主要語言" if sys_lang == 'zh' else "Select the Main Language "
    print(msg)
    TARGET_LANG = language_selection()

    merge_name_to_description(
        names_path=NAMES_FILE,
        desc_path=DESC_FILE,
        output_path=OUTPUT_FILE,
        source_lang=SOURCE_LANG,
        target_lang=TARGET_LANG
    )

    exit_msg = "\n按下 Enter 鍵結束程式..." if sys_lang == 'zh' else "\nPress Enter to exit..."
    input(exit_msg)