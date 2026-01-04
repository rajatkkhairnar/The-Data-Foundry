import pandas as pd
import numpy as np

def create_drifted_data():
    print("Loading Reference Data...")
    df = pd.read_csv('data\synthetic_data.csv')
    
    # SIMULATE DRIFT:
    # 1. Inflation hit: Everyone spends 50% more (Shift in Mean)
    print("Injecting Drift: Increasing amounts by 50%...")
    df['amount'] = df['amount'] * 1.5
    
    # 2. Demographics change: Younger people start using the app
    print("Injecting Drift: Lowering customer age...")
    df['customer_age'] = df['customer_age'] - 10
    
    # Save as 'production.csv' (simulating live data logs)
    output_path = 'data/production.csv'
    df.to_csv(output_path, index=False)
    print(f"Drifted data saved to {output_path}")

if __name__ == "__main__":
    create_drifted_data()