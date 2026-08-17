import pandas as pd
import numpy as np

def calculate_financial_health_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers financial health metrics and risk indicators for banking customers.
    """
    df_metrics = df.copy()

    # 1. Debt-to-Income (DTI) Ratio (%)
    if 'EMI_Amount' in df_metrics.columns and 'Monthly_Income' in df_metrics.columns:
        df_metrics['DTI_Ratio'] = np.where(
            df_metrics['Monthly_Income'] > 0,
            (df_metrics['EMI_Amount'] / df_metrics['Monthly_Income']) * 100,
            0
        )

    # 2. Net Savings Rate (%)
    if all(col in df_metrics.columns for col in ['Monthly_Deposit', 'Monthly_Withdrawal', 'Monthly_Income']):
        df_metrics['Net_Savings_Rate'] = np.where(
            df_metrics['Monthly_Income'] > 0,
            ((df_metrics['Monthly_Deposit'] - df_metrics['Monthly_Withdrawal']) / df_metrics['Monthly_Income']) * 100,
            0
        )

    # 3. Total Relationship Value (TRV)
    trv_cols = ['Account_Balance', 'FD_Amount', 'Investment_Amount']
    existing_trv_cols = [c for c in trv_cols if c in df_metrics.columns]
    if existing_trv_cols:
        df_metrics['Total_Relationship_Value'] = df_metrics[existing_trv_cols].sum(axis=1)

    # 4. Digital Engagement Flag
    if 'Online_Banking_Usage' in df_metrics.columns and 'Mobile_Banking_Usage' in df_metrics.columns:
        df_metrics['Digital_Adoption'] = np.select(
            [
                (df_metrics['Online_Banking_Usage'] == 'Yes') & (df_metrics['Mobile_Banking_Usage'] == 'Yes'),
                (df_metrics['Online_Banking_Usage'] == 'Yes') | (df_metrics['Mobile_Banking_Usage'] == 'Yes')
            ],
            ['Fully Digital', 'Semi Digital'],
            default='Non-Digital'
        )

    # 5. Age Group Categorization
    if 'Age' in df_metrics.columns:
        bins = [17, 30, 45, 60, 100]
        labels = ['18-30', '31-45', '46-60', '60+']
        df_metrics['Age_Group'] = pd.cut(df_metrics['Age'], bins=bins, labels=labels)

    return df_metrics