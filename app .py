
import streamlit as st
import pickle
import pandas as pd
import numpy as np

model = pickle.load(open("insurance_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.title("Life Insurance Approval Prediction System")

age = st.number_input("Age", min_value=18, max_value=100, value=30)

gender = st.selectbox("Gender", ["Male", "Female"])

bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)

children = st.number_input("Children", min_value=0, max_value=10, value=0)

smoker = st.selectbox("Smoker", ["No", "Yes"])

region = st.selectbox(
    "Region",
    ["northeast", "northwest", "southeast", "southwest"]
)

income = st.number_input("Income", min_value=10000, max_value=500000, value=50000)

medical_history = st.selectbox(
    "Medical History",
    ["Average", "Bad", "Good"]
)

exercise = st.selectbox(
    "Exercise",
    ["None", "Occasional", "Regular"]
)

gender = 1 if gender == "Male" else 0
smoker = 1 if smoker == "Yes" else 0

region_map = {
    "northeast": 0,
    "northwest": 1,
    "southeast": 2,
    "southwest": 3
}

medical_map = {
    "Average": 0,
    "Bad": 1,
    "Good": 2
}

exercise_map = {
    "None": 0,
    "Occasional": 1,
    "Regular": 2
}

risk_score = int(age > 50) + int(bmi > 30) + smoker

if income <= 40000:
    income_category = 0
elif income <= 70000:
    income_category = 1
else:
    income_category = 2

if bmi < 18.5:
    bmi_category = 0
elif bmi < 25:
    bmi_category = 1
elif bmi < 30:
    bmi_category = 2
else:
    bmi_category = 3

data = np.array([[
    age,
    gender,
    bmi,
    children,
    smoker,
    region_map[region],
    income,
    medical_map[medical_history],
    exercise_map[exercise],
    risk_score,
    income_category,
    bmi_category
]])

data = scaler.transform(data)

prediction = model.predict(data)

if st.button("Predict"):

    if prediction[0] == 1:
        st.success("Insurance Approved")

    else:
        st.error("Insurance Rejected")
