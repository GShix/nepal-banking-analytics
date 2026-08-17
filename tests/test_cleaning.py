import os
import pandas as pd
import pytest

CLEAN_DATA_PATH = "data/processed/banking_data_clean.csv"

@pytest.fixture
def clean_df():
    assert os.path.exists(CLEAN_DATA_PATH), f"Cleaned data file not found at {CLEAN_DATA_PATH}"
    return pd.read_csv(CLEAN_DATA_PATH)

def test_no_missing_values(clean_df):
    critical_cols = ['Account_Balance', 'Monthly_Income', 'Age', 'Credit_Score']
    for col in critical_cols:
        assert clean_df[col].isnull().sum() == 0, f"Column {col} contains unexpected missing values."

def test_no_duplicate_rows(clean_df):
    assert clean_df.duplicated().sum() == 0, f"Clean dataset contains duplicate rows."

def test_valid_age_range(clean_df):
    assert clean_df['Age'].min() >= 18, f"Minimum age {clean_df['Age'].min()} is below 18."
    assert clean_df['Age'].max() <= 100, f"Maximum age {clean_df['Age'].max()} exceeds 100."

def test_valid_credit_scores(clean_df):
    assert clean_df['Credit_Score'].min() >= 300, f"Found invalid credit score < 300."

def test_currency_symbols_removed(clean_df):
    assert pd.api.types.is_numeric_dtype(clean_df['Account_Balance']), f"Account_Balance is not numeric."