from sdv.evaluation.single_table import evaluate_quality
from sdv.metadata import SingleTableMetadata
import pandas as pd
import json

class ModelEvaluator:
    def __init__(self, real_data_path, synthetic_data_path):
        self.real_df = pd.read_csv(real_data_path)
        self.synth_df = pd.read_csv(synthetic_data_path)
        self.metadata = SingleTableMetadata()
        self.metadata.detect_from_dataframe(self.real_df)
        
        # Ensure ID columns are handled correctly in metadata
        if 'transaction_id' in self.real_df.columns:
            self.metadata.update_column(column_name='transaction_id', sdtype='id')

    def run_evaluation(self):
        """
        Runs the SDV Quality Report.
        Returns a score (0-100%) representing how similar the data is.
        """
        print("--- Running Statistical Evaluation ---")
        
        # 1. Run the Quality Report
        report = evaluate_quality(
            real_data=self.real_df,
            synthetic_data=self.synth_df,
            metadata=self.metadata
        )
        
        # 2. Get the overall score
        score = report.get_score()
        print(f"\nOverall Quality Score: {score:.2%}")
        
        # 3. Get details on column shapes (KS-Test)
        print("\n--- Column Shape Quality ---")
        properties = report.get_properties()
        print(properties)

        return report

    def save_report(self, report, output_path='models/quality_report.pkl'):
        """Saves the visual report object."""
        report.save(output_path)
        print(f"\nReport saved to {output_path}")

if __name__ == "__main__":
    # We need to generate a batch first to compare
    from generator import DataGenerator
    
    # 1. Generate fresh synthetic data
    gen = DataGenerator()
    gen.load_model()
    # Generate same number of rows as real data for fair comparison
    fake_data = gen.generate_batch(n_rows=100)
    fake_data.to_csv('data/synthetic_data.csv', index=False)
    
    # 2. Evaluate
    evaluator = ModelEvaluator(
        real_data_path='P:\AI & ML\The Data flower\data_quality_framework\data\clean_data_2.csv',
        synthetic_data_path='P:\AI & ML\The Data flower\Synthetic_data_generator\data\synthetic_data.csv'
    )
    quality_report = evaluator.run_evaluation()
    evaluator.save_report(quality_report)