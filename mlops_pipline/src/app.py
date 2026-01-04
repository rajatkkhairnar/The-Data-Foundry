from fastapi import FastAPI
import joblib
import pandas as pd
import uvicorn

app = FastAPI()

# Load Model
model = joblib.load('models/classifier.pkl')

@app.get("/")
def home():
    return {"message": "MLOps Pipeline API is running!"}

@app.post("/predict")
def predict(age: int, amount: float):
    # Prepare input for model
    data = pd.DataFrame([[age, amount]], columns=['customer_age', 'amount'])
    
    # Predict
    prediction = model.predict(data)[0]
    
    result = "High Value" if prediction == 1 else "Standard Value"
    return {
        "input": {"age": age, "amount": amount},
        "prediction": result
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)