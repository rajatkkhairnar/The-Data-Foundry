import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train_baseline_model():
    print("Loading Reference Data...")
    df = pd.read_csv('data\synthetic_data.csv')
    
    # Feature Engineering
    # Let's define "High Value" as amount > 300 (Binary Classification)
    df['is_high_value'] = (df['amount'] > 300).astype(int)
    
    # Select Features (Numeric only for simplicity)
    features = ['customer_age', 'amount'] # In real life, we'd encode categories
    X = df[features]
    y = df['is_high_value']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    print("Training Random Forest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Model Accuracy: {accuracy:.2%}")
    
    # Save
    joblib.dump(model, 'models/classifier.pkl')
    print("Model saved to models/classifier.pkl")

if __name__ == "__main__":
    train_baseline_model()