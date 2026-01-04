import sys
import os
import time

# Add the current directory to path so imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from monitor import DriftMonitor
from train_model import train_baseline_model

def run_mlops_pipeline():
    print("=============================================")
    print("   🤖 MLOPS AUTOMATED PIPELINE STARTED       ")
    print("=============================================")

    # 1. Define Paths
    # Ensure these point to where your CSVs actually are
    REF_DATA = 'data/reference.csv'
    PROD_DATA = 'data/production.csv'
    
    # 2. Check for Drift
    print("\n[STEP 1] Checking for Data Drift...")
    monitor = DriftMonitor(REF_DATA, PROD_DATA)
    monitor.run_drift_check()
    monitor.save_report()
    
    is_drifted = monitor.is_drift_detected()
    
    # 3. Decision Logic
    if is_drifted:
        print("\n[ALERT] 🚨 DRIFT DETECTED! Initiating automated retraining...")
        time.sleep(1) # Dramatic pause
        
        print("\n[STEP 2] Retraining Model...")
        # In a real system, we might train on the NEW data (production.csv)
        # For this demo, we just re-run the training script to prove the link works.
        train_baseline_model()
        
        print("\n✅ SUCCESS: Model has been retrained and saved.")
        print("New model version: v2.0 (Simulated)")
        
    else:
        print("\n[OK] System Stable. No action required.")
        print("Model remains at version: v1.0")

    print("\n=============================================")
    print("   🏁 PIPELINE FINISHED                      ")
    print("=============================================")

if __name__ == "__main__":
    run_mlops_pipeline()