import json
import pandas as pd
import numpy as np  # <--- Added numpy import
from datetime import datetime

class QualityReporter:
    def __init__(self):
        self.log = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "initial_health": {},
            "final_health": {},
            "actions_taken": []
        }

    def log_initial_state(self, df: pd.DataFrame, audit_report: dict):
        """Record the state of data before cleaning."""
        self.log["initial_health"] = {
            "rows": len(df),
            "columns": len(df.columns),
            "issues": audit_report
        }

    def log_final_state(self, df: pd.DataFrame, audit_report: dict):
        """Record the state of data after cleaning."""
        self.log["final_health"] = {
            "rows": len(df),
            "columns": len(df.columns),
            "issues": audit_report
        }

    def add_action(self, action_description):
        """Add a specific repair action to the log."""
        self.log["actions_taken"].append(action_description)

    def save_report(self, filename="data_quality_report.json"):
        """Saves the log as a JSON file."""
        
        # --- NEW HELPER FUNCTION ---
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)  # Convert numpy int to python int
            elif isinstance(obj, np.floating):
                return float(obj) # Convert numpy float to python float
            elif isinstance(obj, np.ndarray):
                return obj.tolist() # Convert arrays to lists
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        # ---------------------------

        with open(filename, 'w') as f:
            # We add 'default=convert_numpy' to handle the types automatically
            json.dump(self.log, f, indent=4, default=convert_numpy)
            
        print(f"Report generated: {filename}")