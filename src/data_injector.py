import os
import numpy as np
import pandas as pd

def inject_dirty_data(input_filepath: str, output_filepath: str, seed: int = 42):
    """
    Reads raw banking dataset, introduces ~30% dirty records/anomalies,
    and exports the dirty dataset to CSV.
    """
    np.random.seed(seed)
    
    # Load dataset (handles both CSV and Excel input)
    if input_filepath.endswith('.xlsx') or input_filepath.endswith('.xls'):
        df = pd.read_excel(input_filepath)
    else:
        df = pd.read_csv(input_filepath)
        
    df_dirty = df.copy()
    n_rows = len(df_dirty)
    print(f"Loaded raw dataset with {n_rows} rows.")

    # Select ~30% unique row indices for corruption
    target_corrupt_count = int(n_rows * 0.30)
    corrupt_indices = np.random.choice(n_rows, size=target_corrupt_count, replace=False)

    # Explicitly cast ALL target columns to 'object' dtype
    # to prevent pandas datetime64 / int64 type-safety errors
    target_cols = [
        'Account_Balance', 'Monthly_Income', 'Age', 'Credit_Score', 
        'Loan_Amount', 'Account_Open_Date', 'Last_Transaction_Date'
    ]
    for col in target_cols:
        if col in df_dirty.columns:
            df_dirty[col] = df_dirty[col].astype(str)

    # 1. Currency Strings & Data Type Pollutants (~25% of corrupted set)
    idx_curr = corrupt_indices[:int(target_corrupt_count * 0.25)]
    if 'Account_Balance' in df_dirty.columns:
        df_dirty.loc[idx_curr, 'Account_Balance'] = df_dirty.loc[idx_curr, 'Account_Balance'].apply(
            lambda x: f"NPR {float(x):,.2f}" if (pd.notnull(x) and x != 'nan') else x
        )
    if 'Monthly_Income' in df_dirty.columns:
        df_dirty.loc[idx_curr, 'Monthly_Income'] = df_dirty.loc[idx_curr, 'Monthly_Income'].apply(
            lambda x: f"{x} NPR" if (pd.notnull(x) and x != 'nan') else x
        )

    # 2. Missing & Disguised Nulls (~20% of corrupted set)
    idx_null = corrupt_indices[int(target_corrupt_count * 0.25):int(target_corrupt_count * 0.45)]
    half = len(idx_null) // 2
    if 'Occupation' in df_dirty.columns:
        df_dirty.loc[idx_null[:half], 'Occupation'] = np.random.choice(["N/A", "Unknown", "  "], size=half)
    if 'Education_Level' in df_dirty.columns:
        df_dirty.loc[idx_null[half:], 'Education_Level'] = np.nan

    # 3. Impossible Outliers & Invalid Values (~15% of corrupted set)
    idx_outliers = corrupt_indices[int(target_corrupt_count * 0.45):int(target_corrupt_count * 0.60)]
    third = len(idx_outliers) // 3
    if 'Age' in df_dirty.columns:
        df_dirty.loc[idx_outliers[:third], 'Age'] = np.random.choice(["-5", "-1", "140", "150"], size=third)
    if 'Credit_Score' in df_dirty.columns:
        df_dirty.loc[idx_outliers[third: 2*third], 'Credit_Score'] = "-999"
    if 'Loan_Amount' in df_dirty.columns:
        df_dirty.loc[idx_outliers[2*third:], 'Loan_Amount'] = df_dirty.loc[idx_outliers[2*third:], 'Loan_Amount'].apply(
            lambda x: str(float(x) * -1.5) if (pd.notnull(x) and x != 'nan') else x
        )

    # 4. Whitespace & Text Inconsistencies (~20% of corrupted set)
    idx_text = corrupt_indices[int(target_corrupt_count * 0.60):int(target_corrupt_count * 0.80)]
    if 'City' in df_dirty.columns:
        df_dirty.loc[idx_text, 'City'] = df_dirty.loc[idx_text, 'City'].apply(
            lambda x: f"  {str(x).lower()}  " if pd.notnull(x) else x
        )
    if 'Account_Type' in df_dirty.columns:
        df_dirty.loc[idx_text, 'Account_Type'] = df_dirty.loc[idx_text, 'Account_Type'].apply(
            lambda x: str(x).upper() if pd.notnull(x) else x
        )

    # 5. Invalid Date Formats (~20% of corrupted set)
    idx_dates = corrupt_indices[int(target_corrupt_count * 0.80):]
    if 'Account_Open_Date' in df_dirty.columns:
        df_dirty.loc[idx_dates, 'Account_Open_Date'] = "2025/31/12"  # Invalid month error

    # 6. Duplicate Rows (~5% duplicates added)
    num_duplicates = int(n_rows * 0.05)
    duplicates = df_dirty.sample(n=num_duplicates, random_state=seed)
    df_dirty = pd.concat([df_dirty, duplicates], ignore_index=True)

    # Shuffle dataset rows
    df_dirty = df_dirty.sample(frac=1, random_state=seed).reset_index(drop=True)

    # Export dirty output
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    df_dirty.to_csv(output_filepath, index=False)
    
    print(f"Successfully generated dirty dataset at: '{output_filepath}'")
    print(f"Total Rows (with inserted duplicates): {len(df_dirty)}")

if __name__ == "__main__":
    RAW_PATH = "data/raw/Banking_Data.csv" 
    DIRTY_PATH = "data/dirty/banking_data_dirty.csv"
    
    if not os.path.exists(RAW_PATH) and os.path.exists("data/raw/Banking_Data.xlsx"):
        RAW_PATH = "data/raw/Banking_Data.xlsx"
        
    inject_dirty_data(RAW_PATH, DIRTY_PATH)