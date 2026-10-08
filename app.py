import streamlit as st
import pandas as pd
import base64
from pathlib import Path
import requests

BACKEND_URL = "https://salary-intelligence-platform-1.onrender.com"


# -----------------------------
# Background Image
# -----------------------------

image_path = Path("background.jpeg")

image_base64 = base64.b64encode(
    image_path.read_bytes()
).decode()

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ALL INPUT BOXES */
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stNumberInput"] > div > div,
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #17324d !important;
        border-radius: 12px !important;
        border: 1px solid #b8c7d9 !important;
    }}

    /* Number input text */
    div[data-testid="stNumberInput"] input {{
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #17324d !important;
        -webkit-text-fill-color: #17324d !important;
    }}

    /* Dropdown text */
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {{
        color: #17324d !important;
    }}

    /* Dropdown selected value */
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] {{
        color: #17324d !important;
    }}

    /* Input labels */
    label {{
        color: #17324d !important;
        font-weight: 600 !important;
    }}

    /* Slider label */
    div[data-testid="stSlider"] label {{
        color: #17324d !important;
        font-weight: 600 !important;
    }}

    /* Number input +/- buttons */
    div[data-testid="stNumberInput"] button {{
        background-color: #ffffff !important;
        color: #17324d !important;
    }}

    /* Dropdown menu */
    ul[data-baseweb="menu"] {{
        background-color: #ffffff !important;
    }}

    ul[data-baseweb="menu"] li {{
        background-color: #ffffff !important;
        color: #17324d !important;
    }}

    /* Dropdown hover */
    ul[data-baseweb="menu"] li:hover {{
        background-color: #eef5fb !important;
        color: #17324d !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Title
# -----------------------------

st.title("Intelligent Salary Prediction & Career Insights Platform")

st.write(
    "Enter employee details to generate a compensation estimate."
)


# -----------------------------
# Employee Inputs
# -----------------------------

age = st.number_input(
    "Age",
    min_value=20,
    max_value=60,
    value=25
)

gender = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

education = st.selectbox(
    "Education",
    [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "PhD"
    ]
)

experience = st.number_input(
    "Experience (Years)",
    min_value=0,
    max_value=40,
    value=0
)

job_role = st.selectbox(
    "Job Role",
    [
        "Software Developer",
        "ML Engineer",
        "Operations Executive",
        "Data Scientist",
        "Marketing Executive",
        "Marketing Manager",
        "Digital Marketer",
        "IT Support",
        "Recruiter",
        "System Administrator",
        "Finance Manager",
        "Sales Executive",
        "Operations Manager",
        "Sales Manager",
        "Accountant",
        "Project Coordinator",
        "Business Development Executive",
        "Data Analyst",
        "HR Executive",
        "Financial Analyst",
        "HR Manager"
    ]
)

department = st.selectbox(
    "Department",
    [
        "Finance",
        "Marketing",
        "Sales",
        "Data Science",
        "HR",
        "IT",
        "Operations"
    ]
)

location = st.selectbox(
    "Location",
    [
        "Bengaluru",
        "Delhi",
        "Visakhapatnam",
        "Kakinada",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Mumbai"
    ]
)

company_size = st.selectbox(
    "Company Size",
    [
        "Small",
        "Medium",
        "Large"
    ]
)

performance_score = st.number_input(
    "Performance Score",
    min_value=1,
    max_value=10,
    value=5
)

skills_count = st.number_input(
    "Skills Count",
    min_value=2,
    max_value=15,
    value=5
)

working_hours = st.number_input(
    "Working Hours Per Day",
    min_value=6,
    max_value=12,
    value=8
)


# -----------------------------
# Main Salary Prediction
# -----------------------------

if st.button("Analyze Compensation", key="analyze"):

    employee_data = {
        "Age": age,
        "Gender": gender,
        "Education": education,
        "Experience_Years": experience,
        "Job_Role": job_role,
        "Department": department,
        "Location": location,
        "Company_Size": company_size,
        "Performance_Score": performance_score,
        "Skills_Count": skills_count,
        "Working_Hours_Per_Day": working_hours
    }

    response = requests.post(
        f"{BACKEND_URL}/predict",
        json=employee_data
    )

    if response.status_code == 200:

        result = response.json()

        prediction = result["predicted_salary"]

        st.subheader("Estimated Salary")

        st.metric(
            "Predicted Annual Salary",
            f"₹{prediction:,.0f}"
        )

        st.subheader("Key Factors Influencing Estimate")

        st.write(
            "The model considers multiple employee attributes "
            "when estimating salary."
        )

        st.write(
            "• Experience Years — strongest overall predictor"
        )

        st.write(
            "• Education — contributes to salary differences"
        )

        st.write(
            "• Performance Score — contributes to salary variation"
        )

        st.write(
            "• Department — contributes to salary variation"
        )

        st.write(
            "• Job Role — contributes to salary variation"
        )

    else:

        st.error(
            "Unable to get prediction from the backend."
        )


# -----------------------------
# What-If Salary Simulator
# -----------------------------

st.subheader("What-If Salary Simulator")

st.write(
    "Explore how changing experience or education "
    "may affect the predicted salary."
)


# Experience simulator

sim_experience = st.slider(
    "Experience (Years)",
    min_value=0,
    max_value=40,
    value=experience,
    key="sim_experience"
)

experience_data = {
    "Age": age,
    "Gender": gender,
    "Education": education,
    "Experience_Years": sim_experience,
    "Job_Role": job_role,
    "Department": department,
    "Location": location,
    "Company_Size": company_size,
    "Performance_Score": performance_score,
    "Skills_Count": skills_count,
    "Working_Hours_Per_Day": working_hours
}

experience_response = requests.post(
    f"{BACKEND_URL}/predict",
    json=experience_data
)

if experience_response.status_code == 200:

    experience_result = experience_response.json()

    experience_prediction = experience_result["predicted_salary"]

    st.metric(
        "Salary With Selected Experience",
        f"₹{experience_prediction:,.0f}"
    )

else:

    st.error(
        "Unable to get experience simulation from the backend."
    )


# Education simulator

sim_education = st.selectbox(
    "Choose Education",
    [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "PhD"
    ],
    key="sim_education"
)

education_sim_data = {
    "Age": age,
    "Gender": gender,
    "Education": sim_education,
    "Experience_Years": sim_experience,
    "Job_Role": job_role,
    "Department": department,
    "Location": location,
    "Company_Size": company_size,
    "Performance_Score": performance_score,
    "Skills_Count": skills_count,
    "Working_Hours_Per_Day": working_hours
}

education_response = requests.post(
    f"{BACKEND_URL}/predict",
    json=education_sim_data
)

if education_response.status_code == 200:

    education_result = education_response.json()

    education_prediction = education_result["predicted_salary"]

    st.metric(
        "Salary With Selected Education",
        f"₹{education_prediction:,.0f}"
    )

else:

    st.error(
        "Unable to get education simulation from the backend."
    )


# -----------------------------
# Career Compensation Analytics
# -----------------------------

st.subheader("Career Compensation Analytics")

st.write(
    "Compare model-estimated salary across education levels."
)

education_data = pd.DataFrame({
    "Education": [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "PhD"
    ],
    "Estimated Salary": [
        651569,
        693669,
        755163,
        831725,
        958456
    ]
})

st.bar_chart(
    education_data,
    x="Education",
    y="Estimated Salary"
)


# Department comparison

st.subheader("Department Salary Comparison")

st.write(
    "Compare model-estimated salary across departments."
)

department_data = pd.DataFrame({
    "Department": [
        "IT",
        "Data Science",
        "Finance",
        "HR",
        "Marketing",
        "Operations",
        "Sales"
    ],
    "Estimated Salary": [
        755163,
        807992,
        713765,
        658201,
        684420,
        668132,
        675887
    ]
})

st.bar_chart(
    department_data,
    x="Department",
    y="Estimated Salary"
)


# -----------------------------
# Information Note
# -----------------------------

st.write("")

st.markdown(
    """
    <div style="
        background-color: rgba(255,255,255,0.85);
        padding: 15px;
        border-radius: 12px;
        color: #17324d;
        font-size: 15px;
        text-align: center;
        margin-top: 20px;
    ">
    The analytics show model-estimated salary comparisons
    based on the project dataset and a fixed baseline profile.
    </div>
    """,
    unsafe_allow_html=True
)import streamlit as st
import pandas as pd
import base64
from pathlib import Path
import requests


# -----------------------------
# Background Image
# -----------------------------

image_path = Path("background.jpeg")

image_base64 = base64.b64encode(
    image_path.read_bytes()
).decode()

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* ALL INPUT BOXES */
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stNumberInput"] > div > div,
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #17324d !important;
        border-radius: 12px !important;
        border: 1px solid #b8c7d9 !important;
    }}

    /* Number input text */
    div[data-testid="stNumberInput"] input {{
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #17324d !important;
        -webkit-text-fill-color: #17324d !important;
    }}

    /* Dropdown text */
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {{
        color: #17324d !important;
    }}

    /* Dropdown selected value */
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] {{
        color: #17324d !important;
    }}

    /* Input labels */
    label {{
        color: #17324d !important;
        font-weight: 600 !important;
    }}

    /* Slider label */
    div[data-testid="stSlider"] label {{
        color: #17324d !important;
        font-weight: 600 !important;
    }}

    /* Number input +/- buttons */
    div[data-testid="stNumberInput"] button {{
        background-color: #ffffff !important;
        color: #17324d !important;
    }}

    /* Dropdown menu */
    ul[data-baseweb="menu"] {{
        background-color: #ffffff !important;
    }}

    ul[data-baseweb="menu"] li {{
        background-color: #ffffff !important;
        color: #17324d !important;
    }}

    /* Dropdown hover */
    ul[data-baseweb="menu"] li:hover {{
        background-color: #eef5fb !important;
        color: #17324d !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)
# -----------------------------
# Title
# -----------------------------

st.title("Intelligent Salary Prediction & Career Insights Platform")

st.write(
    "Enter employee details to generate a compensation estimate."
)


# -----------------------------
# Employee Inputs
# -----------------------------

age = st.number_input(
    "Age",
    min_value=20,
    max_value=60,
    value=25
)

gender = st.selectbox(
    "Gender",
    ["Female", "Male"]
)

education = st.selectbox(
    "Education",
    [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "PhD"
    ]
)

experience = st.number_input(
    "Experience (Years)",
    min_value=0,
    max_value=40,
    value=0
)

job_role = st.selectbox(
    "Job Role",
    [
        "Software Developer",
        "ML Engineer",
        "Operations Executive",
        "Data Scientist",
        "Marketing Executive",
        "Marketing Manager",
        "Digital Marketer",
        "IT Support",
        "Recruiter",
        "System Administrator",
        "Finance Manager",
        "Sales Executive",
        "Operations Manager",
        "Sales Manager",
        "Accountant",
        "Project Coordinator",
        "Business Development Executive",
        "Data Analyst",
        "HR Executive",
        "Financial Analyst",
        "HR Manager"
    ]
)

department = st.selectbox(
    "Department",
    [
        "Finance",
        "Marketing",
        "Sales",
        "Data Science",
        "HR",
        "IT",
        "Operations"
    ]
)

location = st.selectbox(
    "Location",
    [
        "Bengaluru",
        "Delhi",
        "Visakhapatnam",
        "Kakinada",
        "Hyderabad",
        "Chennai",
        "Pune",
        "Mumbai"
    ]
)

company_size = st.selectbox(
    "Company Size",
    [
        "Small",
        "Medium",
        "Large"
    ]
)

performance_score = st.number_input(
    "Performance Score",
    min_value=1,
    max_value=10,
    value=5
)

skills_count = st.number_input(
    "Skills Count",
    min_value=2,
    max_value=15,
    value=5
)

working_hours = st.number_input(
    "Working Hours Per Day",
    min_value=6,
    max_value=12,
    value=8
)


# -----------------------------
# Main Salary Prediction
# -----------------------------

if st.button("Analyze Compensation", key="analyze"):

    employee_data = {
        "Age": age,
        "Gender": gender,
        "Education": education,
        "Experience_Years": experience,
        "Job_Role": job_role,
        "Department": department,
        "Location": location,
        "Company_Size": company_size,
        "Performance_Score": performance_score,
        "Skills_Count": skills_count,
        "Working_Hours_Per_Day": working_hours
    }

    response = requests.post(
    "https://salary-intelligence-platform-1.onrender.com/predict",
        json=employee_data
    )

    if response.status_code == 200:

        result = response.json()

        prediction = result["predicted_salary"]

        st.subheader("Estimated Salary")

        st.metric(
            "Predicted Annual Salary",
            f"₹{prediction:,.0f}"
        )

        st.subheader("Key Factors Influencing Estimate")

        st.write(
            "The model considers multiple employee attributes "
            "when estimating salary."
        )

        st.write(
            "• Experience Years — strongest overall predictor"
        )

        st.write(
            "• Education — contributes to salary differences"
        )

        st.write(
            "• Performance Score — contributes to salary variation"
        )

        st.write(
            "• Department — contributes to salary variation"
        )

        st.write(
            "• Job Role — contributes to salary variation"
        )

    else:

        st.error(
            "Unable to get prediction from the backend."
        )


# -----------------------------
# What-If Salary Simulator
# -----------------------------

st.subheader("What-If Salary Simulator")

st.write(
    "Explore how changing experience or education "
    "may affect the predicted salary."
)


# Experience simulator

sim_experience = st.slider(
    "Experience (Years)",
    min_value=0,
    max_value=40,
    value=experience,
    key="sim_experience"
)

experience_data = {
    "Age": age,
    "Gender": gender,
    "Education": education,
    "Experience_Years": sim_experience,
    "Job_Role": job_role,
    "Department": department,
    "Location": location,
    "Company_Size": company_size,
    "Performance_Score": performance_score,
    "Skills_Count": skills_count,
    "Working_Hours_Per_Day": working_hours
}

experience_response = requests.post(
    "https://salary-intelligence-platform-1.onrender.com/predict",
    json=experience_data
)

if experience_response.status_code == 200:

    experience_result = experience_response.json()

    experience_prediction = experience_result["predicted_salary"]

    st.metric(
        "Salary With Selected Experience",
        f"₹{experience_prediction:,.0f}"
    )

else:

    st.error(
        "Unable to get experience simulation from the backend."
    )


# Education simulator

sim_education = st.selectbox(
    "Choose Education",
    [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "PhD"
    ],
    key="sim_education"
)

education_sim_data = {
    "Age": age,
    "Gender": gender,
    "Education": sim_education,
    "Experience_Years": sim_experience,
    "Job_Role": job_role,
    "Department": department,
    "Location": location,
    "Company_Size": company_size,
    "Performance_Score": performance_score,
    "Skills_Count": skills_count,
    "Working_Hours_Per_Day": working_hours
}

education_response = requests.post(
    "https://salary-intelligence-platform-1.onrender.com/predict",
    json=education_sim_data
)

if education_response.status_code == 200:

    education_result = education_response.json()

    education_prediction = education_result["predicted_salary"]

    st.metric(
        "Salary With Selected Education",
        f"₹{education_prediction:,.0f}"
    )

else:

    st.error(
        "Unable to get education simulation from the backend."
    )


# -----------------------------
# Career Compensation Analytics
# -----------------------------

st.subheader("Career Compensation Analytics")

st.write(
    "Compare model-estimated salary across education levels."
)

education_data = pd.DataFrame({
    "Education": [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "PhD"
    ],
    "Estimated Salary": [
        651569,
        693669,
        755163,
        831725,
        958456
    ]
})

st.bar_chart(
    education_data,
    x="Education",
    y="Estimated Salary"
)


# Department comparison

st.subheader("Department Salary Comparison")

st.write(
    "Compare model-estimated salary across departments."
)

department_data = pd.DataFrame({
    "Department": [
        "IT",
        "Data Science",
        "Finance",
        "HR",
        "Marketing",
        "Operations",
        "Sales"
    ],
    "Estimated Salary": [
        755163,
        807992,
        713765,
        658201,
        684420,
        668132,
        675887
    ]
})

st.bar_chart(
    department_data,
    x="Department",
    y="Estimated Salary"
)


# -----------------------------
# Information Note
# -----------------------------

st.write("")

st.markdown(
    """
    <div style="
        background-color: rgba(255,255,255,0.85);
        padding: 15px;
        border-radius: 12px;
        color: #17324d;
        font-size: 15px;
        text-align: center;
        margin-top: 20px;
    ">
    The analytics show model-estimated salary comparisons
    based on the project dataset and a fixed baseline profile.
    </div>
    """,
    unsafe_allow_html=True
)
