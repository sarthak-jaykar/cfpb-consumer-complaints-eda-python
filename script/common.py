"""Shared paths and helpers for the CFPB consumer complaints project."""
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "consumer_complaints.xlsx"
PROCESSED_FILE = Path(tempfile.gettempdir()) / "complaints_clean.csv"
RESULTS = ROOT / "results"
SCREENSHOTS = ROOT / "screenshots"

RESULTS.mkdir(parents=True, exist_ok=True)
SCREENSHOTS.mkdir(parents=True, exist_ok=True)

# Short labels for charts and tables (full names kept in the data)
PRODUCT_SHORT = {
    "Checking or savings account": "Checking / savings",
    "Credit card or prepaid card": "Credit card / prepaid",
    "Credit reporting, credit repair services, or other personal consumer reports": "Credit reporting",
    "Mortgage": "Mortgage",
    "Money transfer, virtual currency, or money service": "Money transfer",
    "Debt collection": "Debt collection",
    "Vehicle loan or lease": "Vehicle loan / lease",
    "Payday loan, title loan, or personal loan": "Payday / personal loan",
    "Student loan": "Student loan",
}
# 2023 contains only January to August (the data ends on 28 Aug 2023)
PARTIAL_YEAR = 2023


def load_features():
    """Load the feature-enriched processed file (written by 03_features.py)."""
    import pandas as pd
    return pd.read_csv(PROCESSED_FILE, low_memory=False, parse_dates=["date_submitted", "date_received"])
