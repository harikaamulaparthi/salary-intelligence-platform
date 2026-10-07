from fastapi import FastAPI
import joblib
import pandas as pd
from pathlib import Path
from pydantic import BaseModel

app = FastAPI()

model_path = Path(__file__).resolve().parent / "salary_intelligence_model.pkl"
model = joblib.load(model_path)


class EmployeeData(BaseModel):
    Age: int
    Gender: str
    Education: str
    Experience_Years: int
    Job_Role: str
    Department: str
    Location: str
    Company_Size: str
    Performance_Score: int
    Skills_Count: int
    Working_Hours_Per_Day: int


@app.post("/predict")
def predict_salary(data: EmployeeData):
    employee = pd.DataFrame([data.model_dump()])
    prediction = model.predict(employee)

    return {
        "predicted_salary": float(prediction[0])
    }
