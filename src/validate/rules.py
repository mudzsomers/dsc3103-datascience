import pandas as pd


def rule_positive_price(df):
    """Flags rows that have a price of zero or negative"""
    neg_prices = df[df["price"] <= 0].copy()
    neg_prices["Reason"] = "Negative Price"
    return neg_prices


def rule_duplicate_ids(df):
    dup_ids = df[df["id"].duplicated(keep=False)].copy()
    dup_ids["Reason"] = "Duplicate ID"
    return dup_ids


def rule_duplicate_rows(df):
    dup_rows = df[df.duplicated(keep=False)].copy()
    dup_rows["Reason"] = "Duplicate Row"
    return dup_rows


def rule_valid_date(df):
    converted_dates = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    bad_dates = df[converted_dates.isna()].copy()
    bad_dates["Reason"] = "Invalid Date"
    return bad_dates


def rule_missing_market(df):
    missing_market = df[df["market"].isna()].copy()
    missing_market["Reason"] = "Missing Market"
    return missing_market


"""def rule_known_commodity(df):
    known = {"maize", "beans"}
    bad_commodity = df[~df["commodities"].str.lower().isin(known)].copy()
    bad_commodity["Reason"] = "Unknown Commodity"
    return bad_commodity """

known_commodities = {"Maize", "Beans"}

def rule_known_commodity(df):
    """Flags commodities that are inconsistently cased/spaced, or genuinely unknown"""
    normalized = df["commodities"].str.strip().str.title()

    inconsistent_mask = (df["commodities"] != normalized) & normalized.isin(known_commodities)
    unknown_mask = ~normalized.isin(known_commodities)

    inconsistent = df[inconsistent_mask].copy()
    inconsistent["Reason"] = "Inconsistent Category"
    inconsistent["Suggested Value"] = normalized[inconsistent_mask]

    unknown = df[unknown_mask].copy()
    unknown["Reason"] = "Unknown Commodity"
    unknown["Suggested Value"] = pd.NA

    return pd.concat([inconsistent, unknown])