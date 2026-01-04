import pandas as pd
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
import pickle
import os

class GANTrainer:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None
        self.metadata = None

    def load_data(self):
        """Loads data and detects metadata (schema)."""
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        
        # SDV needs to know the schema (metadata)
        self.metadata = SingleTableMetadata()
        self.metadata.detect_from_dataframe(self.df)
        
        # Optional: Set primary key if you have one, or remove it for generation
        # If transaction_id is unique, we might want to drop it or let SDV handle it
        if 'transaction_id' in self.df.columns:
            self.metadata.update_column(
                column_name='transaction_id',
                sdtype='id'
            )
            
        print("Metadata detected:")
        print(self.metadata.to_dict())

    def train(self, epochs=300):
        """Trains the CTGAN model."""
        print(f"Training CTGAN for {epochs} epochs. This may take a moment...")
        
        # Initialize the Synthesizer
        self.model = CTGANSynthesizer(
            metadata=self.metadata,
            epochs=epochs,
            verbose=True
        )
        
        self.model.fit(self.df)
        print("Training complete.")

    def save_model(self, output_path='models/transaction_gan.pkl'):
        """Saves the trained model to disk."""
        if self.model is None:
            raise ValueError("Model has not been trained yet. Call train() first.")
        print(f"Saving model to {output_path}...")
        self.model.save(output_path)
        print("Model saved successfully.")

if __name__ == "__main__":
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    trainer = GANTrainer('P:\AI & ML\The Data flower\data_quality_framework\data\clean_data_2.csv')
    trainer.load_data()
    trainer.train(epochs=100) # Quick run for testing
    trainer.save_model()