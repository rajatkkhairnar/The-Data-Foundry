import pandas as pd
import numpy as np

class DataRepairman:
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the Repairman with a pandas DataFrame.
        NOTE: We work on a copy to avoid accidentally mutating the original data
        until we are ready.
        """
        self.df = df.copy()

    def remove_duplicates(self):
        """
        Removes duplicate rows from the dataset.
        """
        initial_count = len(self.df)
        self.df.drop_duplicates(inplace=True)
        final_count = len(self.df)
        
        removed = initial_count - final_count
        print(f"Repair: Removed {removed} duplicate rows.")
        return self.df

    def fill_missing_values(self, method='median'):
        """
        Fills missing values.
        - Numeric columns: Fills with Median (default) or Mean.
        - Categorical (text) columns: Fills with Mode (most frequent value).
        """
        # 1. Identify numeric and categorical columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns

        print(f"Repair: Filling missing values using method='{method}'...")

        # 2. Fix Numeric Columns
        for col in numeric_cols:
            if self.df[col].isnull().sum() > 0:
                if method == 'median':
                    fill_value = self.df[col].median()
                else:
                    fill_value = self.df[col].mean()
                
                self.df[col] = self.df[col].fillna(fill_value)
                print(f"   -> Filled {col} with {fill_value:.2f}")

        # 3. Fix Categorical Columns (Always use Mode)
        for col in categorical_cols:
            if self.df[col].isnull().sum() > 0:
                # Mode returns a series, we take the first element
                fill_value = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(fill_value)
                print(f"   -> Filled {col} with '{fill_value}'")

        return self.df

    def cap_outliers(self, column, limit=3):
        """
        Caps outliers using the Z-Score method.
        Any value > 3 standard deviations from mean is capped.
        """
        if column not in self.df.columns:
            print(f"Warning: Column {column} not found.")
            return

        mean = self.df[column].mean()
        std = self.df[column].std()
        
        # Define thresholds
        upper_bound = mean + (limit * std)
        lower_bound = mean - (limit * std)

        # Count how many we are fixing
        outliers = self.df[(self.df[column] > upper_bound) | (self.df[column] < lower_bound)]
        print(f"Repair: Capping {len(outliers)} outliers in '{column}'.")

        # Cap the values
        self.df[column] = np.where(self.df[column] > upper_bound, upper_bound, self.df[column])
        self.df[column] = np.where(self.df[column] < lower_bound, lower_bound, self.df[column])
        
        return self.df
    
    # Add inside DataRepairman class
    def normalize_text_columns(self):
        """
        Step 9: Data consistency & encoding normalization.
        - Trims whitespace (" NY " -> "NY")
        - Converts to lowercase ("Toys" -> "toys")
        """
        print("Repair: Normalizing text columns (trim & lowercase)...")
        # Select string columns
        str_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in str_cols:
            # 1. Strip whitespace
            self.df[col] = self.df[col].str.strip()
            # 2. Lowercase
            self.df[col] = self.df[col].str.lower()
            print(f"   -> Normalized '{col}'")
            
        return self.df