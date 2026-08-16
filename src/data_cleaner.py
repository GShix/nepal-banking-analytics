import os
import re
import numpy as np
import pandas as pd

class BankDataCleaner:
    def __init__(self, dirty_filepath: str, clean_filepath: str):
        self.dirty_filepath = dirty_filepath
        self.clean_filepath = clean_filepath
        self.df = None

    def load_dirty_data(self):
        if not os.path.exists(self.dirty_filepath):
            raise FileNotFoundError(f"Dirty dataset not found at '{self.dirty_filepath}'")
        self.df = pd.read_csv(self.dirty_filepath, dtype=str)
        print(f"Loaded dirty dataset with {len(self.df)} rows.")

    def remove_duplicates(self):
        initial_len = len(self.df)
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        dropped = initial_len - len(self.df)
        print(f"Removed {dropped} duplicate rows.")

    def clean_currency_and_numerics(self):
        numeric_cols = [
            'Account_Balance', 'Monthly_Income', 'Loan_Amount', 
            'Interest_Rate', 'EMI_Amount', 'Monthly_Deposit', 
            'Monthly_Withdrawal', 'Debit_Card_Usage', 'Credit_Card_Usage',
            'Online_Banking_Usage', 'Mobile_Banking_Usage', 'Transaction_Count',
            'Average_Transaction', 'ATM_Visits', 'FD_Amount', 
            'Insurance_Premium', 'Investment_Amount', 'Age', 'Credit_Score'
        ]

        def clean_val(val):
            if pd.isnull(val) or str(val).strip().lower() in ['nan', 'none', '', 'null']:
                return np.nan
            # Extract digits, minus signs, and decimal points
            cleaned = re.sub(r'[^\d.-]', '', str(val))
            try:
                return float(cleaned) if cleaned != '' else np.nan
            except ValueError:
                return np.nan

        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(clean_val)

        print("Cleaned currency symbols and standardized numerical types.")

    def clean_text_and_categoricals(self):
        text_cols = [
            'Customer_ID', 'Customer_Name', 'Gender', 'City', 'Province',
            'Occupation', 'Education_Level', 'Marital_Status', 'Account_Number',
            'Account_Type', 'Branch_Name', 'Loan_Status', 'Loan_Type',
            'Customer_Segment', 'Risk_Category', 'Churn_Status', 'Relationship_Manager'
        ]

        for col in text_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(
                    lambda x: str(x).strip().title() if pd.notnull(x) and str(x).strip().lower() not in ['nan', 'n/a', 'unknown', ''] else x
                )
                # Standardize disguised null strings back to np.nan or 'Unknown'
                self.df[col] = self.df[col].replace({'  ': np.nan, 'N/A': np.nan, 'Unknown': np.nan, 'Nan': np.nan})

        print("Standardized text casing and stripped leading/trailing whitespaces.")

    def handle_domain_outliers(self):
        # 1. Age must be realistic (18 to 100)
        if 'Age' in self.df.columns:
            invalid_age_mask = (self.df['Age'] < 18) | (self.df['Age'] > 100)
            self.df.loc[invalid_age_mask, 'Age'] = np.nan
            median_age = self.df['Age'].median()
            self.df['Age'] = self.df['Age'].fillna(median_age).astype(int)

        # 2. Credit score logic (Standard range ~300 - 850)
        if 'Credit_Score' in self.df.columns:
            invalid_cs_mask = (self.df['Credit_Score'] < 300) | (self.df['Credit_Score'] > 900)
            self.df.loc[invalid_cs_mask, 'Credit_Score'] = np.nan
            median_cs = self.df['Credit_Score'].median()
            self.df['Credit_Score'] = self.df['Credit_Score'].fillna(median_cs).astype(int)

        # 3. Loan Amount must be non-negative
        if 'Loan_Amount' in self.df.columns:
            self.df['Loan_Amount'] = self.df['Loan_Amount'].abs()

        print("Applied banking domain validation rules & capped impossible outliers.")

    def clean_dates(self):
        date_cols = ['Account_Open_Date', 'Last_Transaction_Date']

        for col in date_cols:
            if col in self.df.columns:
                # Coerce errors to NaT (Not a Time)
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                # Forward-fill invalid dates or fill with mode/median date
                if self.df[col].isnull().sum() > 0:
                    self.df[col] = self.df[col].ffill().bfill()
                # Standardize output string format (YYYY-MM-DD)
                self.df[col] = self.df[col].dt.strftime('%Y-%m-%d')

        print("Parsed dates into standardized YYYY-MM-DD ISO format.")

    def handle_missing_values(self):
        # Categorical imputations
        if 'Occupation' in self.df.columns:
            self.df['Occupation'] = self.df['Occupation'].fillna('Unemployed/Other')
        if 'Education_Level' in self.df.columns:
            self.df['Education_Level'] = self.df['Education_Level'].fillna('Unspecified')

        # Numerical missing values filled with median grouped by Account_Type
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in num_cols:
            if self.df[col].isnull().sum() > 0:
                if 'Account_Type' in self.df.columns:
                    self.df[col] = self.df.groupby('Account_Type')[col].transform(lambda x: x.fillna(x.median()))
                self.df[col] = self.df[col].fillna(self.df[col].median())

        print("Handled all missing and null values programmatically.")

    def run_pipeline(self):
        self.load_dirty_data()
        self.remove_duplicates()
        self.clean_currency_and_numerics()
        self.clean_text_and_categoricals()
        self.handle_domain_outliers()
        self.clean_dates()
        self.handle_missing_values()

        # Save clean data
        os.makedirs(os.path.dirname(self.clean_filepath), exist_ok=True)
        self.df.to_csv(self.clean_filepath, index=False)
        print(f"Data cleaning pipeline completed! Clean dataset saved to: '{self.clean_filepath}'")
        print(f"Final Clean Records: {len(self.df)} rows | Columns: {len(self.df.columns)}")


if __name__ == "__main__":
    DIRTY_DATA_PATH = "data/dirty/banking_data_dirty.csv"
    CLEAN_DATA_PATH = "data/processed/banking_data_clean.csv"

    cleaner = BankDataCleaner(dirty_filepath=DIRTY_DATA_PATH, clean_filepath=CLEAN_DATA_PATH)
    cleaner.run_pipeline()