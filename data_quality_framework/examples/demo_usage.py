import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.audits import DataAuditor
from src.repairs import DataRepairman
from src.reporter import QualityReporter

def run_production_pipeline():
    # 1. Initialize Reporter
    reporter = QualityReporter()
    
    print("=== STEP 1: LOADING DATA ===")
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_data.csv')
    df = pd.read_csv(data_path)
    
    # 2. Initial Audit
    print("Running Initial Audit...")
    auditor = DataAuditor(df)
    initial_issues = auditor.run_full_audit()
    reporter.log_initial_state(df, initial_issues)
    auditor.check_cardinality()

    # 3. Repairs
    print("\nRunning Repairs...")
    repairman = DataRepairman(df)

    # -- Normalize Text Columns
    repairman.normalize_text_columns()
    reporter.add_action("Normalized text (strip & lowercase)")
    
    # -- Fix Duplicates
    repairman.remove_duplicates()
    reporter.add_action("Removed duplicates")
    
    # -- Fix Missing
    repairman.fill_missing_values(method='median')
    reporter.add_action("Filled missing values (Median for num, Mode for cat)")
    
    # -- Fix Outliers
    repairman.cap_outliers(column='amount', limit=3)
    reporter.add_action("Capped outliers in 'amount' column (Z-score > 3)")

    clean_df = repairman.df

    # 4. Final Audit
    print("\nRunning Final Audit...")
    final_auditor = DataAuditor(clean_df)
    final_issues = final_auditor.run_full_audit()
    reporter.log_final_state(clean_df, final_issues)

    # 5. Save Artifacts
    clean_df.to_csv('data/clean_data.csv', index=False)
    reporter.save_report("data/quality_report.json")
    print("\nPipeline Complete. Outputs saved.")
    
if __name__ == "__main__":
    run_production_pipeline()