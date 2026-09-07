import pandas as pd 
from src.validate.rules import  (
    rule_positive_price,
    rule_duplicate_ids,
    rule_duplicate_rows,
    rule_valid_date,
    rule_missing_market,
    rule_known_commodity,
)

df = pd.read_csv("data/raw/prices.csv")

print("=== Positive Price Check ===")
print(rule_positive_price(df))

print("\n=== Duplicate IDs Check ===")
print(rule_duplicate_ids(df))

print("\n=== Duplicate Rows Check ===")
print(rule_duplicate_rows(df))

print("\n=== Valid Date Check ===")
print(rule_valid_date(df))

print("\n=== Missing Market Check ===")
print(rule_missing_market(df))

print("\n=== Known Commodity Check ===")
print(rule_known_commodity(df))