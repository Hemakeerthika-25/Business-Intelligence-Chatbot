# src/preprocess.py
import pandas as pd

def load_dataset(file_path):
    df = pd.read_csv(file_path)
    df.dropna(how='all', inplace=True)  # remove empty rows
    df.columns = [col.strip() for col in df.columns]  # clean column names
    
    # Detect numeric, categorical, datetime columns
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    datetime_cols = df.select_dtypes(include='datetime64').columns.tolist()
    
    # Try parsing date columns automatically
    for col in categorical_cols:
        try:
            df[col] = pd.to_datetime(df[col])
            datetime_cols.append(col)
            categorical_cols.remove(col)
        except:
            pass

    return df, numeric_cols, categorical_cols, datetime_cols

from src.preprocess import load_dataset
df, num_cols, cat_cols, dt_cols = load_dataset("data/sales.csv")
print(df.head(), num_cols, cat_cols, dt_cols)