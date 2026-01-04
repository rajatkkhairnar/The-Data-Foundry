import pandas as pd
import numpy as np
import random
import os

# Seed for reproducibility
np.random.seed(42)

def create_dirty_data():
    # 1. Create clean base data
    row_count = 2000 
    
    data = {
        'transaction_id': [f'TXN_{i}' for i in range(row_count)],
        'customer_age': np.random.randint(18, 70, row_count),
        'amount': np.random.uniform(10.0, 500.0, row_count),
        'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Toys'], row_count),
        'timestamp': pd.date_range(start='2024-01-01', periods=row_count, freq='H')
    }
    
    df = pd.DataFrame(data)

    # 2. Inject Defects (The "Dirt")
    
    # Inject Missing Values (NaN)
    df.loc[0:4, 'customer_age'] = np.nan   # 5 missing ages
    df.loc[10:14, 'category'] = np.nan     # 5 missing categories
    
    # Inject Duplicates
    # We take the first 5 rows and append them to the end
    duplicates = df.head(5)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Inject Outliers
    df.loc[90, 'amount'] = 50000.0  # An impossibly high amount
    df.loc[91, 'customer_age'] = 200 # An impossible age

    # Inject Inconsistent Data
    df.loc[50, 'category'] = "electronics" # Lowercase inconsistency

    print("Dirty dataset generated with:")
    print(f"- {df['customer_age'].isnull().sum()} missing ages")
    print(f"- {len(df) - len(df.drop_duplicates())} duplicates")
    print("- 1 massive outlier in 'amount'")
    
    # Save to data folder
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data.csv')
    df.to_csv(data_path, index=False)
    print(f"\nSaved to {data_path}")

if __name__ == "__main__":
    create_dirty_data()