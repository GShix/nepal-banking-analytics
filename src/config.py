import os

BASE_DIR = "/workspace"

DIRTY_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "dirty",
    "banking_data_dirty.csv"
)

PROCESSED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "banking_data_clean.csv"
)