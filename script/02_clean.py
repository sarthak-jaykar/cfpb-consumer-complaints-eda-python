"""
Step 2: Clean and validate. Nothing is filled or dropped silently.

Rules:
- Dates parsed; forwarding lag = Date received - Date submitted (days). This is the time CFPB took to pass the
  complaint to the company, NOT the company's response time (the dataset does not contain a response date).
- "Timely response?" blank = complaint still in progress (matches the "In progress" count). Kept as blank, not guessed.
- Sub-product and sub-issue blanks are kept as "Not recorded"; the source notes that not all products have sub-issues.
- Company public response blank is kept as "Not recorded".
"""
import pandas as pd
from common import RAW_FILE, PROCESSED_FILE, RESULTS

def main():
    df = pd.read_excel(RAW_FILE, sheet_name="Data")
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_").replace("?", "").replace("-", "_"))
    df["date_submitted"] = pd.to_datetime(df["date_submitted"], errors="raise")
    df["date_received"] = pd.to_datetime(df["date_received"], errors="raise")
    df["forward_lag_days"] = (df["date_received"] - df["date_submitted"]).dt.days

    df["timely_response"] = df["timely_response"].map({"Yes": "Yes", "No": "No"}).fillna("In progress / not recorded")
    df["sub_product"] = df["sub_product"].fillna("Not recorded")
    df["sub_issue"] = df["sub_issue"].fillna("Not recorded")
    df["company_public_response"] = df["company_public_response"].fillna("Not recorded")

    checks = pd.DataFrame({
        "check": ["rows", "Complaint ID unique", "negative forwarding lag (expect 0)",
                  "timely response blank (in progress)", "sub-product not recorded",
                  "sub-issue not recorded", "company public response not recorded",
                  "forwarded on the same day (share, %)"],
        "value": [len(df), bool(df["complaint_id"].is_unique), int((df["forward_lag_days"] < 0).sum()),
                  int((df["timely_response"] == "In progress / not recorded").sum()),
                  int((df["sub_product"] == "Not recorded").sum()),
                  int((df["sub_issue"] == "Not recorded").sum()),
                  int((df["company_public_response"] == "Not recorded").sum()),
                  round(100 * (df["forward_lag_days"] == 0).mean(), 2)],
    })
    print(checks.to_string(index=False))
    df.to_csv(PROCESSED_FILE, index=False)
    print(checks.to_string(index=False))

if __name__ == "__main__":
    main()
