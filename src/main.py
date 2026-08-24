import os
import pandas as pd

from config import DIRTY_DATA_PATH, PROCESSED_DATA_PATH
from data_cleaner import BankDataCleaner
from metrics import calculate_financial_health_metrics


def main():
    print("==================================================")
    print("🚀 NEPAL BANKING ANALYTICS - END TO END PIPELINE")
    print("==================================================\n")

    # --------------------------------------------------
    # STEP 1: Validate Dirty Dataset
    # --------------------------------------------------

    print("STEP 1: Loading 30% Dirty Production Dataset...")

    dirty_data_path = str(DIRTY_DATA_PATH)
    processed_data_path = str(PROCESSED_DATA_PATH)

    if not os.path.exists(dirty_data_path):
        print(
            f"❌ Error: Dirty dataset not found at "
            f"{dirty_data_path}"
        )
        return

    print(f"📁 Dirty dataset found: {dirty_data_path}")
    print("-" * 50)

    # --------------------------------------------------
    # STEP 2: Clean and Normalize Dataset
    # --------------------------------------------------

    print("STEP 2: Executing Data Cleaning & Wrangling Pipeline...")

    cleaner = BankDataCleaner(
        dirty_filepath=dirty_data_path,
        clean_filepath=processed_data_path
    )

    cleaner.run_pipeline()

    print("-" * 50)

    # --------------------------------------------------
    # STEP 3: Engineer Business Metrics
    # --------------------------------------------------

    print("STEP 3: Engineering Analytical Metrics & Segments...")

    if not os.path.exists(processed_data_path):
        print(
            "❌ Error: Processed data file missing "
            "after cleaning phase."
        )
        return

    cleaned_df = pd.read_csv(processed_data_path)

    # Calculate DTI, savings rate, age brackets, etc.
    enriched_df = calculate_financial_health_metrics(
        cleaned_df
    )

    # Save final analytical dataset
    enriched_df.to_csv(
        processed_data_path,
        index=False
    )

    print("📊 Success! Enriched analytical fields generated.")
    print(
        f"📁 Power BI Source Dataset Ready: "
        f"'{processed_data_path}'"
    )
    print(
        f"📈 Total Metrics Processed: "
        f"{len(enriched_df)} rows × "
        f"{len(enriched_df.columns)} columns."
    )

    print("\n==================================================")
    print("✅ PIPELINE EXECUTION SUCCESSFUL")
    print("==================================================")


if __name__ == "__main__":
    main()