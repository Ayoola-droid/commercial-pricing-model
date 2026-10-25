"""First look at the CSO table CPM12 (National Average Price).

Reads data/raw/CPM12.csv and prints its shape, columns, date range,
the list of items, missing values, and the latest prices of the items
a bakery would buy and sell. It changes nothing on disk.
"""

from pathlib import Path

import pandas as pd

RAW_FILE = Path("data") / "raw" / "CPM12.csv"

# Items to look at first: the ingredients of a loaf, and the loaf itself
BAKERY_WORDS = ["flour", "bread", "butter", "eggs", "sugar", "milk"]


def main():
    df = pd.read_csv(RAW_FILE, encoding="utf-8-sig")

    print("=== Shape ===")
    print(f"{len(df):,} rows x {len(df.columns)} columns")

    print("\n=== Columns ===")
    print(list(df.columns))

    print("\n=== First 5 rows ===")
    print(df.head().to_string())

    month_codes = df["TLIST(M1)"]
    print("\n=== Date range ===")
    print(f"From {month_codes.min()} to {month_codes.max()}, "
          f"{month_codes.nunique()} months")

    print("\n=== Units ===")
    print(df["UNIT"].value_counts().to_string())

    items = df["Consumer Item"].unique()
    print(f"\n=== {len(items)} consumer items ===")
    for item in items:
        print(" -", item)

    print("\n=== Missing prices ===")
    missing = df[df["VALUE"].isna()]
    print(f"{len(missing):,} of {len(df):,} rows have no price")
    if len(missing) > 0:
        print("Items with the most missing months:")
        print(missing["Consumer Item"].value_counts().head(10).to_string())

    latest = month_codes.max()
    pattern = "|".join(BAKERY_WORDS)
    bakery = df[
        (df["TLIST(M1)"] == latest)
        & df["Consumer Item"].str.contains(pattern, case=False)
    ]
    print(f"\n=== Bakery items, latest month ({latest}) ===")
    print(bakery[["Consumer Item", "VALUE"]].to_string(index=False))


if __name__ == "__main__":
    main()
