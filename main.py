from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Intelligent Salary Prediction</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #eef2ff, #dbeafe);
                margin: 0;
                padding: 25px;
                color: #172554;
            }

            .container {
                max-width: 700px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 18px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            }

            h1 {
                text-align: center;
                margin-bottom: 8px;
            }

            .subtitle {
                text-align: center;
                color: #64748b;
                margin-bottom: 25px;
            }

            label {
                display: block;
                margin-top: 14px;
                font-weight: bold;
            }

            input, select {
                width: 100%;
                padding: 11px;
                margin-top: 6px;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                box-sizing: border-box;
                font-size: 15px;
            }

            button {
                width: 100%;
                margin-top: 25px;
                padding: 14px;
                border: none;
                border-radius: 9px;
                background: #2563eb;
                color: white;
                font-size: 17px;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                background: #1d4ed8;
            }

            #result {
                margin-top: 25px;
                padding: 20px;
                background: #eff6ff;
                border-radius: 12px;
                text-align: center;
                display: none;
            }

            .salary {
                font-size: 30px;
                font-weight: bold;
                color: #1d4ed8;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <h1>Intelligent Salary Prediction</h1>

            <div class="subtitle">
                Career & Compensation Analytics Platform
            </div>

            <label>Age</label>
            <input id="Age" type="number" value="25">

            <label>Gender</label>
            <select id="Gender">
                <option>Female</option>
                <option>Male</option>
            </select>

            <label>Education</label>
            <select id="Education">
                <option>High School</option>
                <option>Diploma</option>
                <option selected>Bachelor's</option>
                <option>Master's</option>
                <option>PhD</option>
            </select>

            <label>Experience (Years)</label>
            <input id="Experience_Years" type="number" value="0">

            <label>Job Role</label>
            <input id="Job_Role" type="text" value="IT Support">

            <label>Department</label>
            <select id="Department">
                <option>Finance</option>
                <option>Marketing</option>
                <option>Sales</option>
                <option>Data Science</option>
                <option>HR</option>
                <option selected>IT</option>
                <option>Operations</option>
            </select>

            <label>Location</label>
            <select id="Location">
                <option>Bengaluru</option>
                <option>Delhi</option>
                <option selected>Visakhapatnam</option>
                <option>Kakinada</option>
                <option>Hyderabad</option>
                <option>Chennai</option>
                <option>Pune</option>
                <option>Mumbai</option>
            </select>

            <label>Company Size</label>
            <select id="Company_Size">
                <option>Small</option>
                <option selected>Medium</option>
                <option>Large</option>
            </select>

            <label>Performance Score</label>
            <input id="Performance_Score" type="number" min="1" max="10" value="5">

            <label>Skills Count</label>
            <input id="Skills_Count" type="number" min="2" max="15" value="5">

            <label>Working Hours Per Day</label>
            <input id="Working_Hours_Per_Day" type="number" min="6" max="12" value="8">

            <button onclick="predictSalary()">
                Analyze Compensation
            </button>

            <div id="result">
                <div>Estimated Annual Salary</div>
                <div class="salary" id="salary"></div>
            </div>

        </div>

        <script>
        async function predictSalary() {

            const data = {
                Age: Number(document.getElementById("Age").value),
                Gender: document.getElementById("Gender").value,
                Education: document.getElementById("Education").value,
                Experience_Years: Number(document.getElementById("Experience_Years").value),
                Job_Role: document.getElementById("Job_Role").value,
                Department: document.getElementById("Department").value,
                Location: document.getElementById("Location").value,
                Company_Size: document.getElementById("Company_Size").value,
                Performance_Score: Number(document.getElementById("Performance_Score").value),
                Skills_Count: Number(document.getElementById("Skills_Count").value),
                Working_Hours_Per_Day: Number(document.getElementById("Working_Hours_Per_Day").value)
            };

            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            document.getElementById("result").style.display = "block";

            document.getElementById("salary").innerText =
                "₹" + Math.round(result.predicted_salary).toLocaleString("en-IN");
        }
        </script>

    </body>
    </html>
    """


@app.post("/predict")
def predict_salary(data: EmployeeData):

    employee = pd.DataFrame([data.model_dump()])

    prediction = model.predict(employee)

    return {
        "predicted_salary": float(prediction[0])
    }
