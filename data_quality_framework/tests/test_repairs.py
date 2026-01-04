import unittest
import pandas as pd
import numpy as np
import sys
import os

# Fix path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.repairs import DataRepairman

class TestRepairs(unittest.TestCase):
    
    def setUp(self):
        """Runs before every test. Creates a tiny dummy dataframe."""
        self.df = pd.DataFrame({
            'age': [25, 30, np.nan, 30],  # 1 missing, 1 duplicate val
            'city': ['NY', 'LA', 'NY', 'NY']
        })
        self.repairman = DataRepairman(self.df)

    def test_missing_value_fill(self):
        """Test if NaN is actually replaced."""
        self.repairman.fill_missing_values(method='median')
        # Check that there are 0 nulls left in 'age'
        self.assertEqual(self.repairman.df['age'].isnull().sum(), 0)

    def test_duplicate_removal(self):
        """Test if duplicates are removed."""
        # Create a df with explicit duplicate row
        df_dup = pd.DataFrame({'a': [1, 1], 'b': [2, 2]})
        rep = DataRepairman(df_dup)
        rep.remove_duplicates()
        # Should be 1 row left
        self.assertEqual(len(rep.df), 1)

if __name__ == '__main__':
    unittest.main()