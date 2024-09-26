import streamlit as st
import pickle
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
from TGSRTC_Productivity.pipeline.prediction import PredictionPipeline

# Set page configuration
st.set_page_config(page_title="TGSRTC")

# Set up the sidebar with options
st.sidebar.header("ESG Options")
# Assuming option1, option2, and option3 are selected from separate selectboxes
option = st.sidebar.radio("Select your choice", 
                               ["Productivity Dashboard (Data)","Productivity Predictor (AI)","Productivity Factors (AI)",  
                               "Health Dashboard (Data)", "Absenteeism Predictor (AI)", "Health Calculator (AI)", "Health Factors (AI)",
                               "Safety Dashboard (Data)", "Accidents Predictor (AI)"
                               ])

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

def load_csv_data():
    try:
        data = pd.read_csv(Path('artifacts/data_ingestion/TGSRTC_Productivity.csv'))
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
    
data = load_csv_data()


# Define functions for each option
def productivity_predictor():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Productivity Calculator (AI)")
    st.text("Predicting driver productivity in KM based on health parameters")
    
    col1, col2, col3 = st.columns([2,1,2])
    
    with col1:
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
                

def productivity_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Productivity Dashboard (Data)")
     
    # Display the data
    #st.write(data)  

    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            depot_options = data['depot'].unique()  # Get unique depot values
            selected_depot = st.selectbox("Select Depot:", depot_options, key='depot_select')
        
            # Filter the data based on the selected depot
            filtered_data = data[data['depot'] == selected_depot]
            
            # Ensure that employee_id is treated as text
            filtered_data['employee_id'] = filtered_data['employee_id'].astype(str)
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data = filtered_data.sort_values(by='tot_opd_kms', ascending=False)
            
            # Calculate the average of tot_opd_kms
            average_opd_kms = sorted_data['tot_opd_kms'].mean()
        
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                fig, ax = plt.subplots()
                ax.bar(sorted_data['employee_id'], sorted_data['tot_opd_kms'])
                ax.set_xlabel('Employee ID')
                ax.set_ylabel('Annual kilometers per driver')
                ax.set_title(f'Productivity by Employee: {selected_depot}')

                # Hide x-axis tick labels
                ax.set_xticks([])
                
                # Add a red average line
                ax.axhline(average_opd_kms, color='red', linestyle='--', label=f'Average: {average_opd_kms:.2f}')
                
                # Show legend
                ax.legend()
                
                # Display the plot in Streamlit
                st.pyplot(fig)
    else:
            st.error("Failed to load data.") 
    
    #PRODUCTIVITY VS AGE GRAPH
    
    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            depot_options1 = data['depot'].unique()  # Get unique depot values
            selected_depot1 = st.selectbox("Select Depot:", depot_options1, key ='depot_select1')
        
            # Filter the data based on the selected depot
            filtered_data1 = data[data['depot'] == selected_depot1]
            
            # Calculate the average of tot_opd_kms
            average_opd_kms1 = filtered_data1['tot_opd_kms'].mean()
        
            if filtered_data1.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                fig, ax = plt.subplots()
                ax.bar(filtered_data1['age'], filtered_data1['tot_opd_kms'])
                ax.set_xlabel('Age, Years')
                ax.set_ylabel('Annual kilometers per driver')
                ax.set_title(f'Avg productivity by Age: {selected_depot1}')

                # Hide x-axis tick labels
                ax.set_xticks([])
                
                # Add a red average line
                ax.axhline(average_opd_kms1, color='red', linestyle='--', label=f'Average: {average_opd_kms1:.2f}')
                
                # Show legend
                ax.legend()
                
                # Display the plot in Streamlit
                st.pyplot(fig)
    else:
            st.error("Failed to load data.") 
            
    #ABSENTEEISM BY DEPOT
    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            depot_options4 = data['depot'].unique()  # Get unique depot values
            selected_depot4 = st.selectbox("Select Depot:", depot_options4, key='depot_select4')
        
            # Filter the data based on the selected depot
            filtered_data4 = data[data['depot'] == selected_depot4]
            
            # Ensure that employee_id is treated as text
            filtered_data4['employee_id'] = filtered_data4['employee_id'].astype(str)
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data4 = filtered_data4.sort_values(by='absent_days', ascending=False)
            
            # Calculate the average of tot_opd_kms
            average_absent_days = sorted_data4['absent_days'].mean()
        
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                fig, ax = plt.subplots()
                ax.bar(sorted_data4['employee_id'], sorted_data4['absent_days'])
                ax.set_xlabel('Employee ID')
                ax.set_ylabel('Annual absent days per driver')
                ax.set_title(f'Absenteeism by Employee: {selected_depot4}')

                # Hide x-axis tick labels
                ax.set_xticks([])
                
                # Add a red average line
                ax.axhline(average_absent_days, color='red', linestyle='--', label=f'Average: {average_absent_days:.2f}')
                
                # Show legend
                ax.legend()
                
                # Display the plot in Streamlit
                st.pyplot(fig)
    else:
            st.error("Failed to load data.") 

def key_productivity_factors():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Health factors impacting productivity")
    st.text("AI model being developed")
    
def health_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Health Dashboard")
    
    #CREATININE VS AGE
    
    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            depot_options2 = data['depot'].unique()  # Get unique depot values
            selected_depot2 = st.selectbox("Select Depot:", depot_options2, key ='depot_select2')
        
            # Filter the data based on the selected depot
            filtered_data2 = data[data['depot'] == selected_depot2]
            
            # Ensure that employee_id is treated as text
            filtered_data2['employee_id'] = filtered_data2['employee_id'].astype(str)
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data2 = filtered_data2.sort_values(by='creatinine_value', ascending=False)
            
            # Calculate the average of tot_opd_kms
            average_creatinine_value = filtered_data2['creatinine_value'].mean()
            
            if filtered_data2.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                fig, ax = plt.subplots()
                ax.bar(sorted_data2['employee_id'], sorted_data2['creatinine_value'])
                ax.set_xlabel('Employee ID')
                ax.set_ylabel('Creatinine Value')
                ax.set_title(f'Creatinine Value By Age: {selected_depot2}')

                # Hide x-axis tick labels
                ax.set_xticks([])
                
                # Add a red average line
                ax.axhline(average_creatinine_value, color='red', linestyle='--', label=f'Average: {average_creatinine_value:.2f}')
                
                # Show legend
                ax.legend()
                
                # Display the plot in Streamlit
                st.pyplot(fig)
    else:
            st.error("Failed to load data.") 
   
   #BLOOD_PRESSURE VS AGE
   
    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            depot_options3 = data['depot'].unique()  # Get unique depot values
            selected_depot3 = st.selectbox("Select Depot:", depot_options3, key ='depot_select3')
        
            # Filter the data based on the selected depot
            filtered_data3 = data[data['depot'] == selected_depot3]
            
            # Calculate the average of tot_opd_kms
            average_blood_pressure_value = filtered_data3['blood_pressure_diastolic'].mean()
            
            if filtered_data3.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                fig, ax = plt.subplots()
                ax.bar(filtered_data3['age'], filtered_data3['blood_pressure_diastolic'])
                ax.set_xlabel('Age, Years')
                ax.set_ylabel('Blood Pressure Diastolic')
                ax.set_title(f'Blood pressure By Age: {selected_depot3}')

                 # Hide x-axis tick labels
                ax.set_xticks([])
                
                # Add a red average line
                ax.axhline(average_blood_pressure_value, color='red', linestyle='--', label=f'Average: {average_blood_pressure_value:.2f}')
                
                # Show legend
                ax.legend()
                
                # Display the plot in Streamlit
                st.pyplot(fig)
    else:
            st.error("Failed to load data.") 
            
    #BLOOD GLUCOSE VS AGE
   
    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            depot_options5 = data['depot'].unique()  # Get unique depot values
            selected_depot5 = st.selectbox("Select Depot:", depot_options5, key ='depot_select5')
        
            # Filter the data based on the selected depot
            filtered_data5 = data[data['depot'] == selected_depot5]
            
            # Calculate the average of tot_opd_kms
            average_glucose_random_value = filtered_data5['glucose_random_value'].mean()
            
            if filtered_data3.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                fig, ax = plt.subplots()
                ax.bar(filtered_data5['age'], filtered_data5['glucose_random_value'])
                ax.set_xlabel('Age, Years')
                ax.set_ylabel('Blood Glucose')
                ax.set_title(f'Blood Glucose By Age: {selected_depot5}')

                 # Hide x-axis tick labels
                ax.set_xticks([])
                
                # Add a red average line
                ax.axhline(average_glucose_random_value, color='red', linestyle='--', label=f'Average: {average_glucose_random_value:.2f}')
                
                # Show legend
                ax.legend()
                
                # Display the plot in Streamlit
                st.pyplot(fig)
    else:
            st.error("Failed to load data.") 
            
    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            depot_options6 = data['depot'].unique()  # Get unique depot values
            selected_depot6 = st.selectbox("Select Depot:", depot_options6, key ='depot_select6')
        
            # Filter the data based on the selected depot
            filtered_data6 = data[data['depot'] == selected_depot6]
            
            # Calculate the average of tot_opd_kms
            #average_glucose_random_value = filtered_data5['glucose_random_value'].mean()
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data6 = filtered_data6.sort_values(by='final_grading', ascending=True)
            
            if filtered_data6.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                fig, ax = plt.subplots()
                sns.boxplot(x='final_grading', y='glucose_random_value', data=sorted_data6, ax=ax)
                ax.set_xlabel('Health Grade')
                ax.set_ylabel('Blood Glucose')
                ax.set_title(f'Blood Glucose By Health Grade: {selected_depot6}')

                
                # Add a red average line
                #ax.axhline(average_glucose_random_value, color='red', linestyle='--', label=f'Average: {average_glucose_random_value:.2f}')
                
                # Show legend
                ax.legend()
                
                # Display the plot in Streamlit
                st.pyplot(fig)
    else:
            st.error("Failed to load data.") 
            
def absenteeism_calc():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Employee Absenteeism (AI)")
    st.text("Predict leaves based on health records. AI model under development")
    
def health_calc():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Health Calculator (AI)")
    st.text("Predict Health Grade Based on Health Record")
    
def key_health_factors():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Key Health Factors (AI)")
    st.text("Operational factors that impact health. AI model under development")

def safety_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Key Safety Trends (Data)")
    st.text("Important Safety Trends")

def accidents_predictor():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Accidents Predictor (AI)")
    st.text("Predicting accidents based on health and operational data")
    

# Productivity
if option == "Productivity Dashboard (Data)":
    productivity_dashboard()  
    
elif option == "Productivity Predictor (AI)":
    productivity_predictor()
    
elif option == "Productivity Factors (AI)":
    key_productivity_factors()

# Health
    
elif option == "Health Dashboard (Data)":
    health_dashboard() 
    
elif option == "Absenteeism Predictor (AI)":
    absenteeism_calc()
    
elif option == "Health Calculator (AI)":
    health_calc()

elif option == "Health Factors (AI)":
    key_health_factors()
    
    
elif option == "Safety Dashboard (Data)":
    safety_dashboard()
    
elif option == "Accidents Predictor (AI)":
    accidents_predictor()




