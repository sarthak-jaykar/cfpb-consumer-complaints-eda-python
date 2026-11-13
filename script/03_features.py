"""
Step 3: Feature engineering on the cleaned file.

Fields added:
  year, year_month, is_partial_year (2023 ends in August)
  product_short (chart label)
  responded (True when timeliness is known, i.e. Yes or No)
  monetary_relief (company response "Closed with monetary relief")
  forwarded_same_day (forward_lag_days == 0)
"""
import pandas as pd
from common import PROCESSED_FILE, PRODUCT_SHORT, PARTIAL_YEAR

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date_submitted"] = pd.to_datetime(df["date_submitted"])
    df["year"] = df["date_submitted"].dt.year
    df["year_month"] = df["date_submitted"].dt.to_period("M").astype(str)
    df["is_partial_year"] = df["year"] == PARTIAL_YEAR
    df["product_short"] = df["product"].map(PRODUCT_SHORT).fillna(df["product"])
    df["responded"] = df["timely_response"].isin(["Yes", "No"])
    df["timely_yes"] = df["timely_response"].eq("Yes")
    df["monetary_relief"] = df["company_response_to_consumer"].eq("Closed with monetary relief")
    df["forwarded_same_day"] = df["forward_lag_days"].eq(0)
    return df

def main():
    df = pd.read_csv(PROCESSED_FILE, low_memory=False)
    feat = build_features(df)
    feat.to_csv(PROCESSED_FILE, index=False)
    print("Features added:", [c for c in feat.columns if c not in df.columns])

if __name__ == "__main__":
    main()
