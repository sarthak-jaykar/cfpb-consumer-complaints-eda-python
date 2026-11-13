"""
Step 1: Ingest and profile the raw workbook. Reads only; does not change the data.
Prints profiling tables to the console.
"""
import pandas as pd
from common import RAW_FILE, RESULTS

def main():
    df = pd.read_excel(RAW_FILE, sheet_name="Data")
    summary = pd.DataFrame({
        "metric": ["rows", "columns", "full duplicate rows", "duplicate Complaint ID values",
                   "first Date submitted", "last Date submitted", "distinct products", "distinct states"],
        "value": [len(df), df.shape[1], int(df.duplicated().sum()), int(df["Complaint ID"].duplicated().sum()),
                  str(pd.to_datetime(df["Date submitted"]).min().date()),
                  str(pd.to_datetime(df["Date submitted"]).max().date()),
                  df["Product"].nunique(), df["State"].nunique()],
    })
    print(summary.to_string(index=False))
    nulls = pd.DataFrame({"column": df.columns, "null_count": df.isna().sum().values,
                          "null_pct": (100 * df.isna().mean()).round(2).values})
    print(nulls.to_string(index=False))
    print(summary.to_string(index=False))
    print(nulls[nulls.null_count > 0].to_string(index=False))

if __name__ == "__main__":
    main()
