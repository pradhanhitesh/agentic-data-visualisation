import os
import polars as pl
from pathlib import Path

def load_data(filepath: str):
    # Check if file exists
    if not os.path.exists(filepath):
        raise ValueError(f"Specified filepath: {filepath} does not exist.")

    try:
        # Load .csv
        if Path(filepath).suffix == '.csv':
            data = pl.read_csv(filepath, ignore_errors=True, infer_schema_length=100000)
            return data
        
        # Load .xlsx
        if Path(filepath).suffix == ".xlsx":
            data = pl.read_excel(filepath)
            return data
        
    except Exception as e:
        raise AssertionError(e)
    