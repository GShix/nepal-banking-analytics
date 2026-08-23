import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data Paths
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "bank_dataset_dirty.csv"
PROCESSED_DATA_PATH = (
    BASE_DIR / "data" / "processed" / "banking_data_enriched.csv"
)

# Business Constants & Risk Thresholds
HIGH_RISK_DTI_THRESHOLD = 40.0
HIGH_VALUE_ACCOUNT_MIN = 100000.0

# Visual Styling Constants
BRAND_COLORS = {
    "primary": "#2b5c8f",
    "secondary": "#d95f02",
    "neutral": "#7570b3",
}