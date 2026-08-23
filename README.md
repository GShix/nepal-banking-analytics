# 🏦 Nepal Banking & Customer Behavior Analytics

[![Power BI](https://img.shields.io/badge/Power_BI-Report-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

An enterprise-grade, end-to-end analytics application that cleans raw transactional banking data, models key executive metrics, segments customer risk profiles, and serves interactive insights via Streamlit and Power BI. Containerized with Docker for 100% reproducible deployment across any environment.

---

## 📊 Power BI Dashboard

[Here](https://login.microsoftonline.com/457a287e-c649-4355-817e-30f728e578d8/oauth2/v2.0/authorize?client_id=871c010f-5e61-4fb1-83ac-98610a7e9110&scope=https%3A%2F%2Fanalysis.windows.net%2Fpowerbi%2Fapi%2F.default%20openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fapp.powerbi.com%2Fsignin&client-request-id=01a02d13-9bad-7903-a6f2-9d3e66778bd0&response_mode=fragment&client_info=1&clidata=1&nonce=01a02d13-9bae-7bb7-bb58-659e7577f2dc&state=eyJpZCI6IjAxYTAyZDEzLTliYWUtNzliMS1hNDZmLTc0OWE5ZGMzZjU1MiIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D%7C1787462654890.8%3B1787462654893.2%3B1787462653204&x-client-SKU=msal.js.browser&x-client-VER=4.30.0&response_type=code&code_challenge=ByZL7qgXPI7j6eWt6u4abAQq8JLZt5XpOTSrP5raQik&code_challenge_method=S256&site_id=500453&nux=1)

## 📌 Executive Summary

Despite maintaining **$1.11B+ in total portfolio deposits**, retail banking performance faces structural cost inefficiencies due to low digital adoption in key demographics and unmitigated credit risk exposures.

This project delivers:

1. **Data Cleaning & Auditing Engine:** An automated pipeline that detects and fixes structural anomalies, negative values, and inconsistent date formats across 1000+ raw records.
2. **Business Feature Engineering:** DAX and Pandas models calculating **Debt-to-Income (DTI)** ratios, **Total Relationship Value (TRV)**, and **Digital Adoption** metrics.
3. **Interactive Decision Dashboard:** Containerized Streamlit & Power BI reporting suites designed for C-suite decision-making.

---

## 📐 Project Architecture

```text
nepal-banking-analytics/
├── .dockerignore              # Docker build exclusions
├── Dockerfile                 # Image blueprint (Python 3.11 Slim)
├── docker-compose.yml         # Container orchestration and volume mapping
├── requirements.txt           # Python dependencies
├── README.md                  # Comprehensive project documentation
<!-- ├── app/
│   ├── __init__.py            # App package initialisation & logging
│   └── dashboard.py           # Streamlit executive dashboard layer -->
├── src/
│   ├── __init__.py            # Package root exporter
│   └── config.py              # Centralised project paths & thresholds
├── notebooks/
│   └── business_insights.ipynb# Exploratory Data Analysis & statistical verification
└── data/
    ├── raw/                   # Unprocessed dirty banking transactional data
    └── processed/
        └── banking_data_enriched.csv  # Cleansed, feature-engineered dataset
```
