
#%%
import pandas as pd
import matplotlib.pyplot as plt 
#%%
from src.validate import rules # this imports all rules at once other than importing one at a time like from src.validate.rules import rule_positive_price 

raw_path ="data/raw/prices.csv"

def inferred_schema(df):
    print("\n Inferred Schema")
    print("------------------------------------------")
    print(df.dtypes)

def row_count(df):
    print("\n ROW COUNT ")
    print("-----------------------------------------")
    print(len(df))

def missing_values(df):
    print("\n MISSING VALUES PER COLUMN")
    print("----------------------------------------")
    print(df.isna().sum())

def negative_values(df):
    negative_values= rules.rule_positive_price(df)
    print("\n NEGATIVE PRICES ")
    print("----------------------------------------")
    print(len(negative_values))

def duplicate_ids(df):
    dup_ids = rules.rule_duplicate_ids(df)
    print("\n DUPLICATE IDS ")
    print("----------------------------------------")
    print(len(dup_ids))

def duplicate_rows(df):
    dup_rows = rules.rule_duplicate_rows(df)
    print("\n DUPLICATE ROWS ")
    print("------------------------------------------")
    print(len(dup_rows))

def invalid_dates(df):
    bad_dates = rules.rule_valid_date(df)
    print("\n INVALID DATES ")
    print("----------------------------------------")
    print(len(bad_dates))


def commodity_category_issues(df):
    issues = rules.rule_known_commodity(df)
    print("\n COMMODITY CATEGORY ISSUES ")
    print("----------------------------------------")
    print(issues["Reason"].value_counts().reindex(["Inconsistent Category", "Unknown Commodity"], fill_value=0))


def summary_statistics(df):
    print("\n SUMMARY STATISTICS (price) ")
    print("------------------------------------")
    print(df["price"].describe())

def price_histogram(df):
    plt.figure()
    df["price"].hist(bins=30)
    plt.title("Distribution of Price (raw, includes -2000 errors)")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.savefig("docs/price_histogram.png")
    print("\n PLOT SAVED to docs/price_histogram.png")
    print("---------------")


def run_files(path=raw_path):
    df =pd.read_csv(path)
    inferred_schema(df)
    row_count(df)
    missing_values(df)
    negative_values(df)
    duplicate_ids(df)
    duplicate_rows(df)
    invalid_dates(df)
    commodity_category_issues(df)
    summary_statistics(df)
    price_histogram(df)
    
    

if __name__ == "__main__":
    run_files()
    
