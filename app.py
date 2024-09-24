import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from TGSRTC_Productivity.pipeline.prediction import PredictionPipeline

# Set up the sidebar with options
st.sidebar.header("ESG Options")
# Assuming option1, option2, and option3 are selected from separate selectboxes
option = st.sidebar.radio("Select your choice", 
                               ["Productivity Calculator (AI)","Productivity Factors (AI)",  
                                "Productivity Gap (AI)", "Productivity Trends (Data)", 
                               "Health Factors (AI)", "Health Calculator (AI)", 
                                "Employee Absenteeism (AI)", "Health Trends (Data)", 
                               "Safety Factors (AI)", "Safety Trends (Data)"])

# Load the model once globally for optimization
#@st.cache(allow_output_mutation=True)
def load_model():
    try:
        model = PredictionPipeline()
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Model loaded once, reused across predictions
model = load_model()

# Define functions for each option
def productivity_calculator():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Productivity Calculator (AI)")
    st.text("Predict productivity based on health")
    

    # Collect inputs from user
    depot_feature = st.selectbox('Select Depot', ['Mahboobnagar', 'Mahboobabad', 'Ranigunj-I'])
    feature_1 = st.slider('Age', min_value=35.0, max_value=60.0, step=1.0)
    feature_2 = st.slider('Creatinine', min_value=0.0, max_value=2.0, step=.1)
    feature_3 = st.slider('Blood Pressure', min_value=100.0, max_value=220.0, step=1.0)
    feature_4 = st.slider('Blood Sugar', min_value=70.0, max_value=300.0, step=1.0)
    feature_5 = st.slider('Bilirubin', min_value=0.5, max_value=2.0, step=0.1)
    feature_6 = st.slider('Cholestrol', min_value=100.0, max_value=300.0, step=1.0)

    # One-hot encoding the depot feature
    if depot_feature == "Mahboobabad":
        feature_7, feature_8, feature_9 = 1, 0, 0
    elif depot_feature == "Mahboobnagar":
        feature_7, feature_8, feature_9 = 0, 1, 0
    else:
        feature_7, feature_8, feature_9 = 0, 0, 1

    # Store inputs in a data frame
    input_data = pd.DataFrame([[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, 
                                feature_7, feature_8, feature_9]],
                              columns=['age', 'creatinine_value', 'blood_pressure_diastolic', 'glucose_random_value', 
                                       'bilirubin_value', 'total_cholestrol', 
                                       'depot_Mahaboobabad', 'depot_Mahaboobnagar', 'depot_Ranigunj-I'])

    st.subheader('Prediction')
    
    # Prediction button
    if st.button('Predict Performance'):
        if model is not None:
            try:
                # Make prediction
                prediction = model.predict(input_data)
                st.success(f'Annual Driver Productivity (in KM): {prediction[0]}')
            except Exception as e:
                st.error(f"Error during prediction: {e}")
        else:
            st.error("Model could not be loaded.")

    
def key_productivity_factors():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Key Productivity Factors (AI)")
    st.text("Measure and improve productivity using data and AI")
    
def productivity_gap():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Productivity Gap (AI)")
    st.text("Individual targets vs. actual performance")
    
def productivity_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Productivity Dashboard (Data)")
    st.text("KM/Month, Hours, Schedules, Depot")
    
    

def key_health_factors():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Key Health Factors (AI)")
    st.text("Important Factors Impacting Health")
    
def health_calc():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Health Calculator (AI)")
    st.text("Predict Health Grade Based on Health Record")
    
def absenteeism_calc():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Employee Absenteeism (AI)")
    st.text("Predict leaves based on health records")

def health_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Health Dashboard (Data)")
    st.text("Absenteeism, Health Data, Top Improvers")

def key_safety_factors():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Key Factors Factors (AI)")
    st.text("Important Factors Impacting Safety")
    
def safety_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Key Safety Trends (Data)")
    st.text("Important Safety Trends")
    
# Home page
if option == "Productivity Factors (AI)":
    key_productivity_factors()

elif option == "Productivity Calculator (AI)":
    productivity_calculator()

elif option == "Productivity Gap (AI)":
    productivity_gap()
    
elif option == "Productivity Trends (Data)":
    productivity_dashboard()    

elif option == "Health Factors (AI)":
    key_health_factors()
    
elif option == "Health Calculator (AI)":
    health_calc()
    
elif option == "Employee Absenteeism (AI)":
    absenteeism_calc()

elif option == "Health Trends (Data)":
    health_dashboard()

elif option == "Safety Factors (AI)":
    key_safety_factors()
    
elif option == "Safety Trends (Data)":
    safety_dashboard()








