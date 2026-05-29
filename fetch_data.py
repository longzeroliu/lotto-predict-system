import pandas as pd
from datetime import datetime
import os

CSV_PATH = "data/lotto.csv"

today = datetime.now().strftime("%Y-%m-%d")

new_row = {
    "lotto_type": "測試",
    "period": today.replace("-", ""),
    "date": today,
    "num1": 1,
    "num2": 2,
    "num3": 3,
    "num4": 4,
    "num5": 5,
    "num6": 6,
    "special_num": 7
}

if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
else:
    df = pd.DataFrame(columns=[
        "lotto_type",
        "period",
        "date",
        "num1",
        "num2",
        "num3",
        "num4",
        "num5",
        "num6",
        "special_num"
    ])

df = pd.concat([
    df,
    pd.DataFrame([new_row])
], ignore_index=True)

df.to_csv(CSV_PATH, index=False)

print("CSV Updated")
