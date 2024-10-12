import streamlit as st
import pickle
import os
import pandas as pd
import numpy as np
from pathlib import Path
from TGSRTC_Productivity.pipeline.stage_06_model_prediction import ModelPredictionPipeline
import altair as alt

# Set page configuration
st.set_page_config(page_title="TGSRTC")


# Initialize the model prediction pipeline
pipeline = ModelPredictionPipeline()


# Load data from CSV into a pandas DataFrame
data = pipeline.load_and_fetch_data()

selected_depot = st.sidebar.selectbox('Select Depot', ['Mahaboobnagar', 'Mahaboobabad', 'Ranigunj-I'])

# Assuming option1, option2, and option3 are selected from separate selectboxes

# Custom CSS to add space between the radio options
st.markdown("""
    <style>
    .streamlit-expander {
        margin-bottom: 10px;  /* Adjust space between options here */
    }
    div[role="radiogroup"] > label {
        margin-bottom: 15px;  /* Adjust space between radio buttons */
    }
    </style>
    """, unsafe_allow_html=True)

option = st.sidebar.radio("Select your choice:", 
                               ["Productivity Baseline FY2023-24","Productivity Potential (AI Tool)",
                               "Health & Productivity",  
                               "Monthly Productivity Monitoring FY2024-25"
                               ])

# Define functions for each option
def productivity_predictor():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("1. Productivity Calculator (AI)")
    st.text("Predicting driver productivity in KM based on health parameters")
    
    #col1, col2, col3 = st.columns([2,1,2])
    
    #with col1:
        # Collect inputs from user
        #depot_feature = st.selectbox('Select Depot', ['Mahboobnagar', 'Mahboobabad', 'Ranigunj-I'])
        
    feature_age = st.slider('Age', min_value=35.0, max_value=60.0, step=1.0)
    feature_crea = st.selectbox('Creatinine', options=['Normal', 'High'])
    feature_bp = st.selectbox('BP', options=['Normal', 'Elevated', 'Stage-1', 'Stage-2', 'Critical'])
    feature_glu = st.selectbox('Glucose', options=['Normal', 'Pre-Diabetes', 'Diabetes'])
    feature_bili = st.selectbox('Bilirubin', options=['Normal', 'High'])
    feature_chole = st.selectbox('Cholestrol', options=['Normal', 'Borderline', 'High'])
    feature_ECG = st.selectbox('ECG', options=['Within Limits', 'Abnormal'])
    feature_night = st.slider('Night Shift %', min_value=0, max_value=100, step=25)
    feature_palle = st.slider('Pallevelugu Schedules %', min_value=0, max_value=100, step=25)
    feature_cityord = st.slider('City Ordinary %', min_value=0, max_value=100, step=25)
    feature_metrolux = st.slider('Metro Express %', min_value=0, max_value=100, step=25)

    # One-hot encoding for depot
    if selected_depot == "Mahaboobabad":
        feature_depot_mn, feature_depot_rg = 0, 0
    elif selected_depot == "Mahaboobnagar":
        feature_depot_mn, feature_depot_rg = 1, 0
    else:
        feature_depot_mn, feature_depot_rg = 0, 1
        
    # One-hot encoding for creatinine
    feature_crea = 1 if feature_crea == "Normal" else 0
        
    # One-hot encoding for blood pressure
    if feature_bp == "Normal":
        feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 1, 0, 0, 0
    elif feature_bp == "Elevated":
        feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 0, 0, 0
    elif feature_bp == "Stage-1":
        feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 1, 0, 0
    elif feature_bp == "Stage-2":
        feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 0, 1, 0
    else:
        feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 0, 0, 1

    # One-hot encoding for glucose
    if feature_glu == "Normal":
        feature_glu_norm, feature_glu_pre = 1, 0
    elif feature_glu == "Pre-Diabetes":
        feature_glu_norm, feature_glu_pre = 0, 1
    else:
        feature_glu_norm, feature_glu_pre = 0, 0

    # One-hot encoding for bilirubin
    feature_bili = 1 if feature_bili == "Normal" else 0
        
    # One-hot encoding for cholesterol
    if feature_chole == "Normal":
        feature_chole_norm, feature_chole_bord = 1, 0
    elif feature_chole == "Borderline":
        feature_chole_norm, feature_chole_bord = 0, 1
    else:
        feature_chole_norm, feature_chole_bord = 0, 0
        
    # One-hot encoding for ECG
    feature_ECG = 1 if feature_ECG == "Within Limits" else 0

    # Store inputs in a data frame
    input_data = pd.DataFrame([[
                                feature_age, 
                                feature_depot_mn, 
                                feature_depot_rg, 
                                feature_crea, 
                                feature_bp_criti,
                                feature_bp_norm, 
                                feature_bp_stage_1,
                                feature_bp_stage_2,
                                feature_glu_norm,
                                feature_glu_pre, 
                                feature_bili, 
                                feature_chole_bord, 
                                feature_chole_norm, 
                                feature_ECG, 
                                feature_night, 
                                feature_palle, 
                                feature_cityord, 
                                feature_metrolux               
                                ]],
                        
                                columns=[
                                    'age', 
                                    'depot_Mahaboobnagar', 
                                    'depot_Ranigunj-I',
                                    'creatinine_interpret_Normal', 
                                    'blood_pressure_interpret_Hypertension Critical', 
                                    'blood_pressure_interpret_Normal', 
                                    'blood_pressure_interpret_Stage-1 Hypertension', 
                                    'blood_pressure_interpret_Stage-2 Hypertension', 
                                    'glucose_interpret_Normal',
                                    'glucose_interpret_Prediabetes', 
                                    'bilirubin_interpret_Normal',
                                    'cholestrol_interpret_Borderline',
                                    'cholestrol_interpret_Normal',
                                    'ECG_interpret_Within Normal Limits',
                                    'night_percent',
                                    'palle_percent',
                                    'cityord_percent',
                                    'metroexp_percent'
                                    ])
    
    st.subheader('Prediction')

# age,
# depot_Mahaboobnagar,
# depot_Ranigunj-I,
# creatinine_interpret_Normal,
# blood_pressure_interpret_Hypertension Critical,
# blood_pressure_interpret_Normal,
# blood_pressure_interpret_Stage-1 Hypertension,
# blood_pressure_interpret_Stage-2 Hypertension,
# glucose_interpret_Normal,
# glucose_interpret_Prediabetes,
# bilirubin_interpret_Normal,
# cholestrol_interpret_Borderline,
# cholestrol_interpret_Normal,
# ECG_interpret_Within Normal Limits,
# night_percent,
# palle_percent,
# cityord_percent,
# metroexp_percent    
    
    # Prediction button
    if st.button('Predict Performance'):
         
        try:  
            prediction = pipeline.make_prediction(input_data)  # Call the pipeline to make predictions            
            st.success(f'Annual Driver Productivity (in Hours): {prediction[0] * 1000 + 500:.0f}')
        except Exception as e:
            st.error(f"Error during prediction: {e}")
        else:
            st.error("Model could not be loaded.")   
            
    st.header("2. Driver productivity potential (AI Tool)")
    st.write("- See the potential for each driver in hours annually")
    st.write("- Analyse the prediction and discuss with driver")
    st.write("**Note: Accuracy of predictions will improve over time**")
   
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
                
            # Filter the data based on the selected depot
            filtered_data7 = data[data['depot'] == selected_depot]
            
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                               
                filtered_data7['Prediction Value'] = None  # You can also use an empty string ""
                
                # Iterate over each driver in the DataFrame and make predictions
            for index, row in filtered_data7.iterrows():
                # Extract individual features
                feature_age = row['age']
                
                # One-hot encoding for depot
                if row['depot'] == "Mahaboobabad":
                    feature_depot_mn, feature_depot_rg = 0, 0
                elif selected_depot == "Mahaboobnagar":
                    feature_depot_mn, feature_depot_rg = 1, 0
                else:
                    feature_depot_mn, feature_depot_rg = 0, 1
                
                # One-hot encoding for creatinine
                feature_crea = 1 if row['creatinine_interpret'] == "Normal" else 0
                
                # One-hot encoding for blood pressure
                if row['blood_pressure_interpret'] == "Normal":
                    feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 1, 0, 0, 0
                elif row['blood_pressure_interpret'] == "Elevated":
                    feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 0, 0, 0
                elif row['blood_pressure_interpret'] == "Stage-1 Hypertension":
                    feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 1, 0, 0
                elif row['blood_pressure_interpret'] == "Stage-2 Hypertension":
                    feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 0, 1, 0
                else:
                    feature_bp_norm, feature_bp_stage_1, feature_bp_stage_2, feature_bp_criti = 0, 0, 0, 1

                # One-hot encoding for glucose
                feature_glu_norm, feature_glu_pre = 0, 0
                if row['glucose_interpret'] == "Normal":
                    feature_glu_norm, feature_glu_pre = 1, 0
                elif row['glucose_interpret'] == "Prediabetes":
                    feature_glu_norm, feature_glu_pre = 0, 1

                # One-hot encoding for bilirubin
                feature_bili = 1 if row['bilirubin_interpret'] == "Normal" else 0

                # One-hot encoding for cholesterol
                feature_chole_norm, feature_chole_bord = 0, 0
                if row['cholestrol_interpret'] == "Normal":
                    feature_chole_norm, feature_chole_bord = 1, 0
                elif row['cholestrol_interpret'] == "Borderline":
                    feature_chole_norm, feature_chole_bord = 0, 1
                
                # One-hot encoding for ECG
                feature_ECG = 1 if row['ECG_interpret'] == "Within Limits" else 0

                # Extract numeric features
                # Handle division by zero for each feature
                feature_night = (row['night_schedules'] / row['tot_schedules'] * 100) if row['tot_schedules'] > 0 else 0
                feature_palle = (row['palle_schedules'] / row['tot_schedules'] * 100) if row['tot_schedules'] > 0 else 0
                feature_cityord = (row['cityord_schedules'] / row['tot_schedules'] * 100) if row['tot_schedules'] > 0 else 0
                feature_metrolux = (row['metroexp_schedules'] / row['tot_schedules'] * 100) if row['tot_schedules'] > 0 else 0

                # Create a DataFrame row for the current driver with all features
                input_data = pd.DataFrame([[feature_age, feature_depot_mn, feature_depot_rg, feature_crea, feature_bp_criti, feature_bp_norm,
                                            feature_bp_stage_1, feature_bp_stage_2, feature_glu_norm,
                                            feature_glu_pre, feature_bili, feature_chole_bord, feature_chole_norm,
                                            feature_ECG, feature_night, feature_palle, feature_cityord, feature_metrolux]],
                                            columns=[
                                            'age', 'depot_Mahaboobnagar', 'depot_Ranigunj-I','creatinine_interpret_Normal', 'blood_pressure_interpret_Hypertension Critical',
                                            'blood_pressure_interpret_Normal', 'blood_pressure_interpret_Stage-1 Hypertension',
                                            'blood_pressure_interpret_Stage-2 Hypertension', 'glucose_interpret_Normal',
                                            'glucose_interpret_Prediabetes', 'bilirubin_interpret_Normal', 'cholestrol_interpret_Borderline',
                                            'cholestrol_interpret_Normal', 'ECG_interpret_Within Normal Limits', 'night_percent',
                                            'palle_percent', 'cityord_percent', 'metroexp_percent'])

                # Predict the productivity using your prediction pipeline
                prediction = pipeline.make_prediction(input_data)  # Call the prediction model
                
                # Store the predicted value in the DataFrame
                filtered_data7.at[index, 'Predicted Value'] = prediction[0] * 1000 + 500
                
            selected_columns = filtered_data7[['employee_id','final_grading','hours','Predicted Value']]
                
            # Rename the columns
            selected_columns = selected_columns.rename(columns={
                'employee_id': 'Employee ID',
                'final_grading': 'GHC2 Grade',
                'hours': 'Annual Hours',
                'Prediction Value': 'Driver Potential, Hours',
                    
                })
                
            st.write(f"**Driver productivity potential for : {selected_depot}**")
            st.dataframe(selected_columns)  
    else:
            st.error("Failed to load data.") 
                

def productivity_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("1. Annual Depot Productivity FY 2023-24, KM")
    st.write("- Some drivers have very high KM/Year; many drivers have low productivity")
    st.write("- On the graph, identify the drivers with very high KM and with very low KM")  
    st.write("- Highly stressed drivers are at risk of burnout")  
    st.write("- Reasons for low productivity needs to be understood and addressed")  
    # Display the data
    #st.write(data)  

    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            #depot_options = data['depot'].unique()  # Get unique depot values
            #selected_depot = st.selectbox("Select Depot:", depot_options, key='depot_select')
            
            # Filter the data based on the selected depot
            filtered_data = data[data['depot'] == selected_depot]
            
            # Ensure that employee_id is treated as text
            filtered_data['employee_id'] = filtered_data['employee_id'].astype(str)
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data = filtered_data.sort_values(by='tot_opd_kms', ascending=False)
            
            # Calculate the average of tot_opd_kms
            median_opd_kms = sorted_data['tot_opd_kms'].median()
            
            # Calculate a dynamic width based on the number of bars (employee IDs)
            num_bars = len(sorted_data)
            bar_width = 10  # You can adjust this value to make the bars wider or narrower
            chart_width = num_bars * bar_width
        
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                                
                # Create a bar chart using Altair with hover annotations and sorted data
                bar_chart = alt.Chart(sorted_data).mark_bar().encode(
                    x=alt.X('employee_id', sort=None, title='Employee ID', 
                            axis=alt.Axis(ticks=False, labels=False)),  # Remove tick marks and set label angle to prevent truncation
                    y=alt.Y('tot_opd_kms', title='Total OPD Kilometers'),  # Add label for y-axis
                    tooltip=['employee_id', 'tot_opd_kms']
                ).properties(
                    title=f'Productivity by Employee: {selected_depot}',  # Correctly display selected depot in the title
                    width=chart_width
                )

                # Create a red dotted line at the median value
                median_line = alt.Chart(pd.DataFrame({'median_opd_kms': [median_opd_kms]})).mark_rule(
                    color='red',
                    strokeDash=[5, 5]  # Dotted line
                ).encode(
                    y='median_opd_kms:Q'  # Specify the y-axis for the median line
                )

                # Combine the bar chart and the median line
                final_chart = bar_chart + median_line

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
                st.error("Failed to load data.") 
    
               
    #ABSENTEEISM BY DEPOT
    # Check if data loaded correctly
    st.header("2. Annual Depot Absenteeism FY 2023-24, Days")
    st.write("- Some drivers have very high absenteeism (Absent+Leave+Sick Leave); many drivers have low absenteeism")
    st.write("- On the graph identify the derivers with very high and very low absenteeism")
    st.write("- Reasons for high absenteeism should be understood; very low absenteeism should also be discouraged")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            #depot_options4 = data['depot'].unique()  # Get unique depot values
            #selected_depot4 = st.selectbox("Select Depot:", depot_options4, key='depot_select4')
        
            # Filter the data based on the selected depot
            filtered_data4 = data[data['depot'] == selected_depot]
            
            # Ensure that employee_id is treated as text
            filtered_data4['employee_id'] = filtered_data4['employee_id'].astype(str)
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data4 = filtered_data4.sort_values(by='hours', ascending=False)
            
            # Calculate the average of tot_opd_kms
            median_hours = sorted_data4['hours'].median()
        
            num_bars = len(sorted_data4)
            bar_width = 10  # You can adjust this value to make the bars wider or narrower
            chart_width = num_bars * bar_width
        
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                                
                # Create a bar chart using Altair with hover annotations and sorted data
                bar_chart = alt.Chart(sorted_data4).mark_bar().encode(
                    x=alt.X('employee_id', sort=None, title='Employee ID', 
                            axis=alt.Axis(ticks=False, labels=False)),  # Remove tick marks and set label angle to prevent truncation
                    y=alt.Y('hours', title='Total Absent Days - A+L+SL'),  # Add label for y-axis
                    tooltip=['employee_id', 'hours']
                ).properties(
                    title=f'Absenteeism by Employee: {selected_depot}',  # Correctly display selected depot in the title
                    width=chart_width
                )

                # Create a red dotted line at the median value
                median_line = alt.Chart(pd.DataFrame({'median_hours': [median_hours]})).mark_rule(
                    color='red',
                    strokeDash=[5, 5]  # Dotted line
                ).encode(
                    y='median_hours:Q'  # Specify the y-axis for the median line
                )

                # Combine the bar chart and the median line
                final_chart = bar_chart + median_line

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 


    #PRODUCTIVITY IN HOURS
    # Check if data loaded correctly
    st.header("3. Annual Depot Productivity FY 2023-24, Hours")

    st.write("- Hours is a better measure of productivity as normalizes the different bus services like slow city routes and fast inter city services etc.")
    st.write("- Go to the graph to identify the really over worked employees and employees who are unable to work")
    
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            #depot_options8 = data['depot'].unique()  # Get unique depot values
            #selected_depot8 = st.selectbox("Select Depot:", depot_options8, key='depot_select8')
        
            # Filter the data based on the selected depot
            filtered_data8 = data[data['depot'] == selected_depot]
            
            # Ensure that employee_id is treated as text
            filtered_data8['employee_id'] = filtered_data8['employee_id'].astype(str)
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data8 = filtered_data8.sort_values(by='hours', ascending=False)
            
            # Calculate the average of tot_opd_kms
            median_hours = sorted_data8['hours'].median()
        
            num_bars = len(sorted_data8)
            bar_width = 10  # You can adjust this value to make the bars wider or narrower
            chart_width = num_bars * bar_width
        
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                                
                # Create a bar chart using Altair with hover annotations and sorted data
                bar_chart = alt.Chart(sorted_data8).mark_bar().encode(
                    x=alt.X('employee_id', sort=None, title='Employee ID', 
                            axis=alt.Axis(ticks=False, labels=False)),  # Remove tick marks and set label angle to prevent truncation
                    y=alt.Y('hours', title='Total Hours'),  # Add label for y-axis
                    tooltip=['employee_id', 'hours']
                ).properties(
                    title=f'Annual Productivity by Employee (Hours): {selected_depot}',  # Correctly display selected depot in the title
                    width=chart_width
                )

                # Create a red dotted line at the median value
                median_line = alt.Chart(pd.DataFrame({'median_hours': [median_hours]})).mark_rule(
                    color='red',
                    strokeDash=[5, 5]  # Dotted line
                ).encode(
                    y='median_hours:Q'  # Specify the y-axis for the median line
                )

                # Combine the bar chart and the median line
                final_chart = bar_chart + median_line

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.")
            
                       
# Productivity by Cholestrol Level
    st.header("4. Annual Depot Productivity (Hours) FY 2023-24 by Cholestrol Level (GHC2)")
    st.write("- Blue box indicates where most drivers productivity levels are")
    st.write("- Red circles indicate individual depot drivers")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            #depot_options7 = data['depot'].unique()  # Get unique depot values
            #selected_depot7 = st.selectbox("Select Depot:", depot_options7, key ='depot_select7')
        
            # Filter the data based on the selected depot
            filtered_data7 = data[data['depot'] == selected_depot]
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data7 = filtered_data7.sort_values(by='final_grading', ascending=True)
            
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data7).mark_boxplot(size=60).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('tot_opd_kms:Q', title='Annual KMs Per Driver')
                ).properties(
                    title=f'Annual KMs By Cholestrol Level: {selected_depot}'
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data7).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('tot_opd_kms:Q', title='Annual KMs Per Driver'),
                    tooltip=['employee_id', 'tot_opd_kms']
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('tot_opd_kms:Q', title='Annual KMs Per Driver')
                )
                
                # Combine both the box plot and the swarm plot
                final_chart = box_plot + swarm_plot

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 

# PAbsenteeism by Cholestrol Level
    st.header("5. Annual Depot Absenteeism (Days) FY 2023-24 by Cholestrol Level (GHC2)")
    st.write("- Blue box indicates where most drivers absent levels are")
    st.write("- Red circles indicate individual depot drivers")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            #depot_options7 = data['depot'].unique()  # Get unique depot values
            #selected_depot7 = st.selectbox("Select Depot:", depot_options7, key ='depot_select7')
        
            # Filter the data based on the selected depot
            filtered_data7 = data[data['depot'] == selected_depot]
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data7 = filtered_data7.sort_values(by='final_grading', ascending=True)
            
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data7).mark_boxplot(size=60).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('hours:Q', title='Absent Days - A+L+SL')
                ).properties(
                    title=f'Annual Absent Days By Cholestrol Level: {selected_depot}'
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data7).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('final_grading:N'),
                    y=alt.Y('hours:Q'),
                    tooltip=['employee_id', 'hours']
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level', axis=alt.Axis(labelAngle=0)),
                    #y=alt.Y('hours:Q', title='Annual absent days Per Driver')
                )
                
                # Combine both the box plot and the swarm plot
                final_chart = box_plot + swarm_plot

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 


    # DRIVER DATA
    st.header("6. Driver productivity data")
    st.write("- See their relative performance in the above graphs")
    st.write("- Discuss reasons for performance")
    st.write("- Sort the date in the table by clicking on the header")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
                
            # Filter the data based on the selected depot
            filtered_data7 = data[data['depot'] == selected_depot]
            
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                selected_columns = filtered_data7[['employee_id','tot_opd_kms','hours','absent_days','final_grading']]
                # Display the table in Streamlit
                
                # Rename the columns
                selected_columns = selected_columns.rename(columns={
                    'employee_id': 'Employee ID',
                    'tot_opd_kms': 'Annual KM',
                    'hours': 'Annual Hours',
                    'absent_days': 'Annual Absent Days',
                    'final_grading': 'GHC2 Grade'
                })
                
                st.write(f"**Driver Productivity and Health Data FY 2023-24 for : {selected_depot}**")
                st.dataframe(selected_columns)  
    else:
            st.error("Failed to load data.") 



def health_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("1. Benchmarking health and productivity of a specific driver")
    
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
            #depot_options7 = data['depot'].unique()  # Get unique depot values
            #selected_depot7 = st.selectbox("Select Depot:", depot_options7, key ='depot_select7')
        
            # Filter the data based on the selected depot
            filtered_data7 = data[data['depot'] == selected_depot]
            
            # Get the employee_id column for the selected depot
            employee_ids = filtered_data7['employee_id'].tolist()
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data7 = filtered_data7.sort_values(by='final_grading', ascending=True)
            
            # Create a selection box with employee_ids from the filtered depot
            selected_employee = st.sidebar.selectbox("Select a depot driver", employee_ids)
            st.write(f"Yellow dot in the graph below shows the selected employee: {selected_employee}")
                        
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data7).mark_boxplot(size=60).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('tot_opd_kms:Q', title='Annual KMs Per Driver')
                ).properties(
                    title=f'Annual KMs By Cholestrol Level: {selected_depot}'
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data7).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('tot_opd_kms:Q', title='Annual KMs Per Driver'),
                    tooltip=['employee_id', 'tot_opd_kms']
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('tot_opd_kms:Q', title='Annual KMs Per Driver')
                )
                
                # Highlight the selected employee with a larger yellow dot
                highlighted_employee = alt.Chart(sorted_data7[sorted_data7['employee_id'] == selected_employee]).mark_point(
                    color='yellow',
                    size=250, filled=True
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('tot_opd_kms:Q'),
                    tooltip=['employee_id', 'tot_opd_kms']
                )

                # Combine the box plot, swarm plot, highlighted employee point, and the custom legend
                final_chart = (box_plot + swarm_plot + highlighted_employee)
              
                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 
    
    #HOURS OF A SPECIFIC DRIVER        
    st.header("2. Benchmarking health and hours of a specific driver")
    st.write(f"Yellow dot in the graph below shows the selected employee: {selected_employee}")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
                                    
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data7).mark_boxplot(size=60).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('hours:Q', title='Annual hours per Driver')
                ).properties(
                    title=f'Annual hours By Cholestrol Level: {selected_depot}'
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data7).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('hours:Q', title='Annual hours per Driver'),
                    tooltip=['employee_id', 'hours']
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('hours:Q', title='Annual hours per Driver')
                )
                
                # Highlight the selected employee with a larger yellow dot
                highlighted_employee = alt.Chart(sorted_data7[sorted_data7['employee_id'] == selected_employee]).mark_point(
                    color='yellow',
                    size=250, filled=True
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('hours:Q'),
                    tooltip=['employee_id', 'hours']
                )

                # Combine the box plot, swarm plot, highlighted employee point, and the custom legend
                final_chart = (box_plot + swarm_plot + highlighted_employee)
              
                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 
    
    
    #ABSENTEEISM OF A SPECIFIC DRIVER        
    st.header("3. Benchmarking health and absenteeism of a specific driver")
    st.write(f"Yellow dot in the graph below shows the selected employee: {selected_employee}")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
                                    
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data7).mark_boxplot(size=60).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('hours:Q', title='Annual Absenteeism per Driver')
                ).properties(
                    title=f'Annual Absenteeism By Cholestrol Level: {selected_depot}'
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data7).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('hours:Q', title='Annual Absenteeism per Driver'),
                    tooltip=['employee_id', 'hours']
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('hours:Q', title='Annual Absenteeism per Driver')
                )
                
                # Highlight the selected employee with a larger yellow dot
                highlighted_employee = alt.Chart(sorted_data7[sorted_data7['employee_id'] == selected_employee]).mark_point(
                    color='yellow',
                    size=250, filled=True
                ).encode(
                    x=alt.X('final_grading:N', title='Cholestrol Level'),
                    y=alt.Y('hours:Q'),
                    tooltip=['employee_id', 'hours']
                )

                # Combine the box plot, swarm plot, highlighted employee point, and the custom legend
                final_chart = (box_plot + swarm_plot + highlighted_employee)
              
                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 
            
    #GLUCOSE OF A SPECIFIC DRIVER        
    st.header("4. Benchmarking Glucose and hours of a specific driver")
    st.write(f"Yellow dot in the graph below shows the selected employee: {selected_employee}")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
                                    
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data7).mark_boxplot(size=60).encode(
                    x=alt.X('glucose_interpret:N', title='Sugar Level', sort=['Normal', 'Prediabetes', 'Diabetes']),
                    y=alt.Y('hours:Q', title='Annual hours per Driver')
                ).properties(
                    title=f'Annual hours By Sugar Level: {selected_depot}'
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data7).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('glucose_interpret:N', title='Sugar Level', sort=['Normal', 'Prediabetes', 'Diabetes']),
                    y=alt.Y('hours:Q', title='Annual hours per Driver'),
                    tooltip=['employee_id', 'hours']
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('glucose_interpret:N', title='Sugar Level', axis=alt.Axis(labelAngle=0), sort=['Normal', 'Prediabetes', 'Diabetes']),
                    y=alt.Y('hours:Q', title='Annual hours per Driver')
                )
                
                # Highlight the selected employee with a larger yellow dot
                highlighted_employee = alt.Chart(sorted_data7[sorted_data7['employee_id'] == selected_employee]).mark_point(
                    color='yellow',
                    size=250, filled=True
                ).encode(
                    x=alt.X('glucose_interpret:N', title='Sugar Level', sort=['Normal', 'Prediabetes', 'Diabetes']),
                    y=alt.Y('hours:Q'),
                    tooltip=['employee_id', 'hours']
                )

                # Combine the box plot, swarm plot, highlighted employee point, and the custom legend
                final_chart = (box_plot + swarm_plot + highlighted_employee)
              
                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 
            
    #BP OF A SPECIFIC DRIVER        
    st.header("5. Benchmarking BP and hours of a specific driver")
    st.write(f"Yellow dot in the graph below shows the selected employee: {selected_employee}")
    st.write("test")
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        # Create a depot filter
                                    
            if filtered_data7.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data7).mark_boxplot(size=60).encode(
                    x=alt.X('blood_pressure_interpret:N', title='BP Level', sort=['Normal','Elevated','Stage-1 Hypertension','Stage-2 Hypertension','Hypertension Critical']),
                    y=alt.Y('hours:Q', title='Annual hours per Driver')
                ).properties(
                    title=f'Annual hours By BP Level: {selected_depot}'
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data7).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('blood_pressure_interpret:N', title='BP Level', sort=['Normal','Elevated','Stage-1 Hypertension','Stage-2 Hypertension','Hypertension Critical']),
                    y=alt.Y('hours:Q', title='Annual hours per Driver'),
                    tooltip=['employee_id', 'hours']
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('blood_pressure_interpret:N', title='BP Level', axis=alt.Axis(labelAngle=0), sort=['Normal','Elevated','Stage-1 Hypertension','Stage-2 Hypertension','Hypertension Critical']),
                    y=alt.Y('hours:Q', title='Annual hours per Driver')
                )
                
                # Highlight the selected employee with a larger yellow dot
                highlighted_employee = alt.Chart(sorted_data7[sorted_data7['employee_id'] == selected_employee]).mark_point(
                    color='yellow',
                    size=250, filled=True
                ).encode(
                    x=alt.X('blood_pressure_interpret:N', title='BP Level', sort=['Normal','Elevated','Stage-1 Hypertension','Stage-2 Hypertension','Hypertension Critical']),
                    y=alt.Y('hours:Q'),
                    tooltip=['employee_id', 'hours']
                )

                # Combine the box plot, swarm plot, highlighted employee point, and the custom legend
                final_chart = (box_plot + swarm_plot + highlighted_employee)
              
                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 

            
def monthly_productivity_dashboard():
    st.title("TGSRTC   ESG   DASHBOARD")
    st.header("Monthly Productivity Monitoring FY2024-25")
    st.text("Monthly monitoring of productivity trends")
    
    

# Productivity
if option == "Productivity Baseline FY2023-24":
    productivity_dashboard()  
    
elif option == "Productivity Potential (AI Tool)":
    productivity_predictor()
    
elif option == "Health & Productivity":
    health_dashboard() 
    
elif option == "Monthly Productivity Monitoring FY2024-25":
    monthly_productivity_dashboard()
    




