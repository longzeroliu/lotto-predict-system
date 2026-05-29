import pandas as pd
import json

df = pd.read_csv("data/lotto.csv")

result = {
    "total_records": len(df)
}

with open(
    "data/statistics.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=4
    )

print("statistics updated")
