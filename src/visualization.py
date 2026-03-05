# src/visualization.py
import matplotlib.pyplot as plt

def plot_response(df, col, keywords, numeric_cols, cat_cols, dt_cols):
    if col in numeric_cols:
        plt.figure(figsize=(8,5))
        if "trend" in keywords or "over time" in keywords:
            # If datetime column exists, plot over time
            dt_col = None
            for c in dt_cols:
                dt_col = c
                break
            if dt_col:
                df.plot(x=dt_col, y=col)
            else:
                df[col].plot(kind='line')
        else:
            df[col].hist()
        plt.title(col)
        plt.show()
    
    elif col in cat_cols:
        plt.figure(figsize=(8,5))
        df[col].value_counts().head(10).plot(kind='bar')
        plt.title(col)
        plt.show()