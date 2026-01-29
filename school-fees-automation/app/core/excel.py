import pandas as pd
from pathlib import Path


def load_school_data(path: str):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")
    return pd.read_excel(p)
