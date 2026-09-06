import pandas as pd
from src.validate import rules

raw_path = "data/raw/prices.csv"
clean_path = "data/processed/prices_clean.parquet"


def clean_data(path=raw_path):
    df = pd.read_csv(path)
    log = []

    # 1. Negative prices -> reject (can't guess a real price)
    bad_price = rules.rule_positive_price(df)
    df = df.drop(bad_price.index)
    log.append(f"Rejected {len(bad_price)} rows with negative price")

    # 2. Duplicate rows -> reject the extra copies
    df = df.drop_duplicates(keep="first")
    log.append("Rejected exact duplicate rows, kept first occurrence")

    # 3. Duplicate ids -> reject rows with clashing ids
    bad_ids = rules.rule_duplicate_ids(df)
    df = df.drop(bad_ids.index)
    log.append(f"Rejected {len(bad_ids)} rows with duplicate id")

    # 4. Invalid dates -> reject (can't guess a real date)
    bad_dates = rules.rule_valid_date(df)
    df = df.drop(bad_dates.index)
    log.append(f"Rejected {len(bad_dates)} rows with invalid date")

    # 5. Missing market -> impute with "Unknown"
    missing_count = df["market"].isna().sum()
    df["market"] = df["market"].fillna("Unknown")
    log.append(f"Imputed {missing_count} missing market values with 'Unknown'")

    # 6. Inconsistent commodity casing -> normalize
    df["commodities"] = df["commodities"].str.lower().str.capitalize()
    log.append("Normalized commodity casing to Title Case (e.g. 'Maize', 'Beans')")

    df.to_parquet(clean_path, index=False)
    log.append(f"Saved cleaned data to {clean_path}")

    for entry in log:
        print(entry)

    return df, log


if __name__ == "__main__":
    clean_data()