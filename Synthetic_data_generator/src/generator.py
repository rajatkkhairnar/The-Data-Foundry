from sdv.single_table import CTGANSynthesizer
from sdv.sampling import Condition
import pandas as pd
import os

class DataGenerator:
    def __init__(self, model_path='models/transaction_gan.pkl'):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """Loads the pre-trained CTGAN model."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}. Run trainer.py first.")
        
        print(f"Loading model from {self.model_path}...")
        self.model = CTGANSynthesizer.load(self.model_path)
        print("Model loaded.")

    def generate_batch(self, n_rows=1100):
        """
        Generates 'n' rows of synthetic data that mimic the original distribution.
        """
        print(f"Generating {n_rows} rows of synthetic data...")
        synthetic_data = self.model.sample(num_rows=n_rows)
        return synthetic_data

    def generate_rare_events(self, column_name, column_value, n_rows=400):
        """
        CONDITIONALLY samples data.
        Forces the model to generate rows where 'column_name' == 'column_value'.
        Useful for upsampling rare classes (e.g., specific defects).
        """
        print(f"Generating {n_rows} rows where {column_name}='{column_value}'...")
        
        # Create a condition
        condition = Condition(
            num_rows=n_rows,
            column_values={column_name: column_value}
        )
        
        # Sample with the condition
        synthetic_data = self.model.sample_from_conditions(
            conditions=[condition]
        )
        return synthetic_data

# ... (Keep the class DataGenerator code exactly the same) ...

if __name__ == "__main__":
    # Test the generator
    gen = DataGenerator()
    gen.load_model()
    
    # 1. Generate a large batch (e.g., 2000 rows)
    print("Generating full synthetic dataset...")
    full_batch = gen.generate_batch(2000)
    
    # SAVE IT! 
    output_path = 'data/synthetic_data.csv'
    full_batch.to_csv(output_path, index=False)
    print(f"✅ Saved synthetic data to: {output_path}")

    # 2. Generate Rare Events (Optional extra file)
    print("Generating rare events (Electronics)...")
    rare_batch = gen.generate_rare_events('category', 'electronics', 100)
    
    # SAVE IT!
    rare_output_path = 'data/rare_electronics.csv'
    rare_batch.to_csv(rare_output_path, index=False)
    print(f"✅ Saved rare events to: {rare_output_path}")