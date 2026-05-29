import pandas as pd
import json
import os

CSV_PATH = "data/lotto.csv"
JSON_PATH = "data/statistics.json"


def get_all_numbers(df):
    """展開 num1~num6 成單一序列"""

    return pd.concat([
        df["num1"],
        df["num2"],
        df["num3"],
        df["num4"],
        df["num5"],
        df["num6"]
    ])


def analyze_lotto(df_lotto):
    """分析單一彩券"""

    result = {}

    # 總期數
    result["draw_count"] = len(df_lotto)

    # 全部號碼
    all_nums = get_all_numbers(df_lotto)

    # 出現次數
    counts = all_nums.value_counts().sort_values(ascending=False)

    # 熱門號碼 Top10
    result["hot_numbers"] = counts.head(10).index.tolist()

    # 冷門號碼 Top10
    result["cold_numbers"] = counts.sort_values().head(10).index.tolist()

    # 熱門號碼詳細次數
    result["hot_number_count"] = {
        str(k): int(v)
        for k, v in counts.head(20).items()
    }

    # 奇偶比例
    odd_count = sum(all_nums % 2 == 1)
    even_count = sum(all_nums % 2 == 0)

    result["odd_even_ratio"] = {
        "odd": int(odd_count),
        "even": int(even_count)
    }

    # 最近30期
    recent = df_lotto.tail(30)

    recent_nums = get_all_numbers(recent)

    recent_counts = recent_nums.value_counts()

    result["recent_30_hot"] = (
        recent_counts.head(10)
        .index
        .tolist()
    )

    result["recent_30_cold"] = (
        recent_counts.sort_values()
        .head(10)
        .index
        .tolist()
    )

    # 特別號統計
    if "special_num" in df_lotto.columns:

        special_counts = (
            df_lotto["special_num"]
            .value_counts()
            .sort_values(ascending=False)
        )

        result["special_hot"] = (
            special_counts.head(5)
            .index
            .tolist()
        )

        result["special_cold"] = (
            special_counts.sort_values()
            .head(5)
            .index
            .tolist()
        )

    return result


def main():

    if not os.path.exists(CSV_PATH):
        print("找不到 lotto.csv")
        return

    df = pd.read_csv(CSV_PATH)

    required_columns = [
        "lotto_type",
        "num1",
        "num2",
        "num3",
        "num4",
        "num5",
        "num6",
        "special_num"
    ]

    for col in required_columns:
        if col not in df.columns:
            print(f"缺少欄位: {col}")
            return

    statistics = {}

    lotto_types = (
        df["lotto_type"]
        .dropna()
        .unique()
    )

    for lotto_type in lotto_types:

        temp = df[
            df["lotto_type"] == lotto_type
        ]

        statistics[lotto_type] = analyze_lotto(temp)

        print(
            f"完成分析: {lotto_type} "
            f"({len(temp)} 期)"
        )

    with open(
        JSON_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            statistics,
            f,
            ensure_ascii=False,
            indent=4
        )

    print("statistics.json 已更新")


if __name__ == "__main__":
    main()
