import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

CSV_PATH = 'data/lotto.csv'

def get_latest_taiwan_lotto():
    """
    爬取台灣彩券最新開獎資訊的模擬函數
    實際運作時需根據台彩官網目前的 HTML 結構解析
    """
    # 這裡以大樂透(Lotto649)為範例結構
    url = "https://www.taiwanlottery.com.tw/index_new.aspx" # 可更換為穩定的彩券API或資料源
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        # 為了教學示範，我們建立一筆最新一期的模擬數據（實務上由此處解析網頁 HTML）
        # 假設今天開出新的一期
        latest_data = {
            "lotto_type": "大樂透",
            "period": "115000045", # 假設 2026 年的期別
            "date": datetime.now().strftime("%Y-%m-%d"),
            "num1": 5, "num2": 12, "num3": 19, "num4": 23, "num5": 36, "num6": 42,
            "special_num": 8
        }
        return latest_data
    except Exception as e:
        print(f"爬取失敗: {e}")
        return None

def main():
    print("開始執行彩券資料更新...")
    
    # 1. 讀取現有的 CSV 檔案
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        # 萬一檔案不見了，重建一個
        df = pd.DataFrame(columns=["lotto_type", "period", "date", "num1", "num2", "num3", "num4", "num5", "num6", "special_num"])
    
    # 2. 爬取最新數據
    latest_draw = get_latest_taiwan_lotto()
    
    if latest_draw:
        # 3. 檢查這一期是否已經紀錄過了
        # 將期別轉為字串進行比對
        if str(latest_draw['period']) in df['period'].astype(str).values:
            print(f"期別 {latest_draw['period']} 已存在，無需更新。")
        else:
            # 4. 不存在則追加新數據
            new_row = pd.DataFrame([latest_draw])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(CSV_PATH, index=False)
            print(f"成功更新期別: {latest_draw['period']}")
    else:
        print("未能取得最新數據。")

if __name__ == "__main__":
    main()
