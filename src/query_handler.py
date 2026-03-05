from fuzzywuzzy import process

def match_column(keyword, columns):
    matched_col, score = process.extractOne(keyword, columns)
    if score > 60:  
        return matched_col
    return None

import pandas as pd

def handle_query(df, numeric_cols, cat_cols, dt_cols, keywords):
    response = ""
    
    # Determine column from keywords
    col = None
    for k in keywords:
        col = match_column(k, df.columns)
        if col:
            break
    
    if not col:
        return "Sorry, I couldn't detect a column in your query."
    
    # Numeric column analysis
    if col in numeric_cols:
        if "max" in keywords or "highest" in keywords or "top" in keywords:
            val = df[col].max()
            response = f"The highest {col} is {val}"
        elif "min" in keywords or "lowest" in keywords:
            val = df[col].min()
            response = f"The lowest {col} is {val}"
        elif "average" in keywords or "mean" in keywords:
            val = df[col].mean()
            response = f"The average {col} is {val:.2f}"
        else:
            response = f"Summary statistics for {col}:\n{df[col].describe()}"
    
    # Categorical column analysis
    elif col in cat_cols:
        top = df[col].value_counts().head(5)
        response = f"Top values in {col}:\n{top.to_dict()}"
    
    # Datetime analysis
    elif col in dt_cols:
        response = f"Date range for {col}: {df[col].min()} to {df[col].max()}"
    
    return response