import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

CSV_PATH = 'data/lotto.csv'

def get_latest_lotto_data():
    """
    同時爬取大樂透與威力彩的最新開獎資訊
    """
    url = "https://www.taiwanlottery.com.tw/index_new.aspx" 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    results = []
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # --- 1. 解析大樂透 (Lotto649) ---
        try:
            lotto_period = soup.find("span", {"id": "Lotto649Control_history_dlGrid_Lotto649_DrawTerm_0"}).text.strip()
            lotto_date = soup.find("span", {"id": "Lotto649Control_history_dlGrid_Lotto649_DDate_0"}).text.strip()
            lotto_balls = [int(soup.find("span", {"id": f"Lotto649Control_history_dlGrid_No{i}_0"}).text.strip()) for i in range(1, 7)]
            lotto_special = int(soup.find("span", {"id": "Lotto649Control_history_dlGrid_No7_0"}).text.strip())
            
            results.append({
                "lotto_type": "大樂透", "period": lotto_period, "date": lotto_date,
                "num1": lotto_balls[0], "num2": lotto_balls[1], "num3": lotto_balls[2],
                "num4": lotto_balls[3], "num5": lotto_balls[4], "num6": balls[5],
                "special_num": lotto_special
            })
        except Exception as e:
            print(f"大樂透解析失敗: {e}")

        # --- 2. 解析威力彩 (SuperLotto) ---
        try:
            super_period = soup.find("span", {"id": "SuperLotto638Control_history_dlGrid_SuperLotto638_DrawTerm_0"}).text.strip()
            super_date = soup.find("span", {"id": "SuperLotto638Control_history_dlGrid_SuperLotto638_DDate_0"}).text.strip()
            super_balls = [int(soup.find("span", {"id": f"SuperLotto638Control_history_dlGrid_No{i}_0"}).text.strip()) for i in range(1, 7)]
            super_special = int(soup.find("span", {"id": "SuperLotto638Control_history_dlGrid_No7_0"}).text.strip())
            
            results.append({
                "lotto_type": "威力彩", "period": super_period, "date": super_date,
                "num1": super_balls[0], "num2": super_balls[1], "num3": super_balls[2],
                "num4": super_balls[3], "num5": super_balls[4], "num6": super_balls[5],
                "special_num": super_special
            })
        except Exception as e:
            print(f"威力彩解析失敗: {e}")
            
        return results
    except Exception as e:
        print(f"網路連線失敗: {e}")
        return []

def main():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
    else:
        df = pd.DataFrame(columns=["lotto_type", "period", "date", "num1", "num2", "num3", "num4", "num5", "num6", "special_num"])
    
    latest_draws = get_latest_lotto_data()
    
    updated = False
    for draw in latest_draws:
        # 同時比對「彩券類型」與「期別」，避免大樂透和威力彩期別撞號
        is_exist = df[(df['lotto_type'] == draw['lotto_type']) & (df['period'].astype(str) == str(draw['period']))]
        
        if is_exist.empty:
            new_row = pd.DataFrame([draw])
            df = pd.concat([df, new_row], ignore_index=True)
            print(f"成功更新 【{draw['lotto_type']}】 期別: {draw['period']}")
            updated = True
        else:
            print(f"【{draw['lotto_type']}】 期別 {draw['period']} 已存在，跳過。")
            
    if updated:
        df.to_csv(CSV_PATH, index=False)

if __name__ == "__main__":
    main()
