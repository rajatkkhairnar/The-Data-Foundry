import pandas as pd
import os
import json
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# NEW API IMPORTS
from evidently import Report
from evidently.presets import DataDriftPreset

class DriftMonitor:
    def __init__(self, reference_path, production_path):
        self.reference = pd.read_csv(reference_path)
        self.production = pd.read_csv(production_path)
        self.report = None
        self.report_result = None  # Store the result here

    def run_drift_check(self):
        print("Running Drift Detection (Evidently AI v0.7+)...")
        
        # 1. Define the Report (The Recipe)
        self.report = Report(metrics=[
            DataDriftPreset(), 
        ])
        
        # 2. Run and Capture the Result (The Meal)
        # CRITICAL FIX: We assign the output to 'self.report_result'
        self.report_result = self.report.run(
            reference_data=self.reference, 
            current_data=self.production
        )
        print("Drift check complete.")

    def save_report(self, output_dir='reports'):
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Save HTML
        html_path = os.path.join(output_dir, 'drift_dashboard.html')
        
        # CRITICAL FIX: Call save_html on the RESULT object
        self.report_result.save_html(html_path)
        print(f"Dashboard saved to: {html_path}")
        
        

    def is_drift_detected(self):
        # CRITICAL FIX: Call as_dict on the RESULT object
        result = self.report_result.dict()
        
        try:
            # Loop through metrics to find the drift flag
            for metric in result['metrics']:
                if 'dataset_drift' in metric.get('result', {}):
                    return metric['result']['dataset_drift']
        except KeyError:
            print("Warning: Could not find drift flag.")
            
        return False

if __name__ == "__main__":
    monitor = DriftMonitor(
        reference_path='data/synthetic_data.csv',
        production_path='data/production.csv'
    )
    monitor.run_drift_check()
    monitor.save_report()
    
    if monitor.is_drift_detected():
        print("\n[ALERT] 🚨 CRITICAL DRIFT DETECTED! Retraining recommended.")
    else:
        print("\n[OK] ✅ Data looks stable.")