import pandas as pd
import sys
import os

# Add the root directory to sys.path so Python can find our 'src' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.audits import DataAuditor

# 1. Load the dirty data
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data.csv')
df = pd.read_csv(data_path)

# 2. Initialize the Auditor
auditor = DataAuditor(df)

# 3. Run the scan
audit_results = auditor.run_full_audit()

print("\nFinal Audit Report Dictionary:")
print(audit_results)