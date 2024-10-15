import streamlit as st
import pickle
import os
import pandas as pd
import numpy as np
from pathlib import Path
from TGSRTC_Productivity.pipeline.stage_06_model_prediction import ModelPredictionPipeline
import altair as alt

# Set page configuration
st.set_page_config(page_title="TGSRTC ESG")

# Initialize the model prediction pipeline
pipeline = ModelPredictionPipeline()

# Load data from CSV into a pandas DataFrame
data = pipeline.load_and_fetch_data()

# Extract distinct depot values
distinct_depots = data['depot'].dropna().unique()

selected_depot = st.sidebar.selectbox('Select Depot:', distinct_depots)

# Filter the data based on the selected depot
filtered_data = data[data['depot'] == selected_depot]

# Extract employee_IDs for the selected depot
employee_ids = filtered_data['employee_id'].dropna().unique()

# Show employee_IDs in another selectbox
selected_employee_id = st.sidebar.selectbox('Select Employee ID:', employee_ids)

# Custom CSS to add space between the radio options
st.markdown("""
    <style>
    .streamlit-expander {
        margin-bottom: 20px;  /* Adjust space between options here */
    }
    div[role="radiogroup"] > label {
        margin-bottom: 20px;  /* Adjust space between radio buttons */
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")

option = st.sidebar.radio("**PRODUCTIVITY + HEALTH:**", 
                                ["STEP 1: SET BASELINE",
                                "STEP 2: SET TARGETS (AI)",  
                                "STEP 3: TRACK IMPROVEMENT"
                                ])


##PREDICTION
def productivity_predictor():
    
    st.title("📊 **TGSRTC ESG Dashboard**")
    st.subheader("*HEALTH + PRODUCTIVITY*")
    st.markdown("---")  # Divider line for better sectioning
    
    # Monthly Depot Productivity (KM)
    st.header("**1. Productivity Predictor (AI Tool)**")
    st.markdown(
        """
        <div style='background-color: #f0f0f5; padding: 10px; border-radius: 10px;'>
            <p>Predicting driver productivity in hours based on health & operational parameters</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing for visual clarity

    # Header for the form
    st.subheader("**Driver Health and Productivity Inputs**")

    # Group 1: Medical Information
    st.markdown("**Medical Metrics**")

    # Use columns to arrange the input fields side by side
    col1, col2, col3 = st.columns(3)

    with col1:
        feature_age = st.slider('Age', min_value=35.0, max_value=60.0, step=1.0)
        feature_crea = st.selectbox('Creatinine', options=['Normal', 'High'], help="Select the driver's creatinine levels")

    with col2:
        feature_bp = st.selectbox('Blood Pressure (BP)', options=['Normal', 'Elevated', 'Stage-1', 'Stage-2', 'Critical'], help="Select the driver's blood pressure stage")
        feature_glu = st.selectbox('Glucose', options=['Normal', 'Pre-Diabetes', 'Diabetes'], help="Select the driver's glucose levels")

    with col3:
        feature_bili = st.selectbox('Bilirubin', options=['Normal', 'High'], help="Select the driver's bilirubin levels")
        feature_chole = st.selectbox('Cholesterol', options=['Normal', 'Borderline', 'High'], help="Select the driver's cholesterol levels")
        feature_ECG = st.selectbox('ECG', options=['Within Limits', 'Abnormal'], help="Select the driver's ECG status")

    # Add some space
    st.write("")

    # Group 2: Schedule Percentages
    st.markdown("**Driver Shift and Schedule Metrics**")

    # Use columns for schedule-related inputs
    col4, col5 = st.columns(2)

    with col4:
        feature_night = st.slider('Night Shift %', min_value=0, max_value=100, step=25, help="Percentage of night shifts handled by the driver")
        feature_palle = st.slider('Pallevelugu Schedules %', min_value=0, max_value=100, step=25, help="Percentage of Pallevelugu schedules handled by the driver")

    with col5:
        feature_cityord = st.slider('City Ordinary %', min_value=0, max_value=100, step=25, help="Percentage of City Ordinary schedules handled by the driver")
        feature_metrolux = st.slider('Metro Express %', min_value=0, max_value=100, step=25, help="Percentage of Metro Express schedules handled by the driver")

    # Optional: You can add a submit button for form completion
    st.write("")
    
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

    # Prediction button
    if st.button('Predict Potential (Hours)'):
        try:  
            prediction = pipeline.make_prediction(input_data)  # Call the pipeline to make predictions            
            st.success(f'Annual Driver Productivity (in Hours): {prediction[0] * 1000 + 500:.0f}')
        except Exception as e:
            st.error(f"Error during prediction: {e}")
    
    
        # Monthly Depot Productivity (KM)
        
    st.markdown("---")  # Divider line for better sectioning
    st.header("**2. Driver productivity potential (AI Tool)**")
    st.markdown(
        """
        <div style='background-color: #f0f0f5; padding: 10px; border-radius: 10px;'>
            <p>RM & DM: Use this tool to assess the productivity potential of an individual driver or depot</p>
            <p>RM & DM: Accuracy of this tool will improve as more depots get added</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing for visual clarity
           
       
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
            
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                filtered_data['Prediction Value'] = None  # You can also use an empty string ""
                
                # Iterate over each driver in the DataFrame and make predictions
            for index, row in filtered_data.iterrows():
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
                filtered_data.at[index, 'Predicted Value'] = prediction[0] * 1000 + 500
                
            selected_columns = filtered_data[['employee_id','final_grading','hours','Predicted Value']]
                
            # Rename the columns
            selected_columns = selected_columns.rename(columns={
                'employee_id': 'Employee ID',
                'final_grading': 'GHC2 Grade',
                'hours': 'Annual Hours',
                'Predicted Value': 'Driver Potential, Hours'  # Correct renaming here
            })

            # Now apply styling to the DataFrame
            styled_table = selected_columns.style.format({
                'Annual Hours': '{:,.0f}',  # Format Annual Hours with commas
                'Driver Potential, Hours': '{:,.0f}'  # Format Driver Potential with commas
            }).background_gradient(
                subset=['Driver Potential, Hours'], cmap='Blues'  # Color scale for Driver Potential
            ).highlight_max(
                subset=['Driver Potential, Hours'], color='lightgreen'  # Highlight highest potential
            ).highlight_min(
                subset=['Driver Potential, Hours'], color='lightcoral'  # Highlight lowest potential
            ).set_properties(**{
                'text-align': 'center',  # Center-align all text
                'font-weight': 'bold'  # Make text bold
            }).set_table_styles([{
                'selector': 'thead th',
                'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-size', '14px')]  # Style the header
            }])

            # Display the table with a title
            st.write(f"**Driver Productivity Potential for: {selected_depot}**")
            st.dataframe(styled_table, width=800)
    else:
            st.error("Failed to load data.") 
                

#DEPOT PRODUCTIVITY
def depot_productivity_dashboard():
    # Page title and subtitle
    st.title("📊 **TGSRTC ESG Dashboard**")
    st.subheader("🔬 *Health + Productivity*")

    # Divider for clear sectioning
    st.markdown("---")

    # Section 1: Productivity Baseline
    st.header("**1. Productivity Baseline (KM/Year), FY2023-24**")

    st.markdown("""
    - **RM & DM**: Understand why there is a significant difference among drivers.
    - **RM & DM**: Identify areas for improvement in the current scheduling process.
    - **RM, DM & Doctors**: Investigate the health reasons behind low performance and explore ways to support affected drivers.
    """)
    
    # Check if data loaded correctly
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:

            # Ensure that employee_id is treated as text
            filtered_data['employee_id'] = filtered_data['employee_id'].astype(str)
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data = filtered_data.sort_values(by='tot_opd_kms', ascending=False)
            
            # Calculate the average of tot_opd_kms
            average_opd_kms = sorted_data['tot_opd_kms'].mean()
            
                            # Format the value to have no decimals and comma separators
            formatted_value = f"{int(average_opd_kms):,}"

            # Use Streamlit's markdown with custom HTML and CSS for styling
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;  /* Light grey background for a clean look */
                    padding: 20px;  /* Increased padding for better spacing */
                    border-radius: 10px;  /* Rounded corners for a modern feel */
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
                    width: 320px;  /* Slightly wider box for better readability */
                    margin: 20px auto;  /* Center the box and add top/bottom margin */
                    text-align: center;
                ">
                    <p style="
                        font-size: 14px;  /* Slightly larger text for better readability */
                        color: #333333;  /* Darker font color for contrast */
                        margin-bottom: 10px;  /* More space below the title */
                    ">
                        <strong>Productivity Baseline (KM/Year)</strong>
                    </p>
                    <p style="
                        font-size: 40px;  /* Larger font for the main value */
                        font-weight: bold; 
                        color: #2c3e50;  /* Darker shade for the number */
                        margin-bottom: 0;
                    ">
                        {formatted_value}
                    </p>
                </div>
                """, unsafe_allow_html=True
            )

            # Adding space below for better structure
            st.write("")
            st.write("")
            
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
                    tooltip=[
                                alt.Tooltip('employee_id', title='Employee ID'),  # Custom label for employee ID
                                alt.Tooltip('tot_opd_kms', title='Annual KM')  # Custom label for total operational kilometers
                    ],
                    color=alt.condition(
                    alt.datum.employee_id == str(selected_employee_id),  # Condition to match the selected employee
                    alt.value('red'),  # Highlight color if condition is true
                    alt.value('steelblue')  # Default color for other bars
                    )
                ).properties(
                        title=alt.TitleParams(
                                                text=f'Productivity by driver (KM/Year): {selected_depot}',  # Correctly display selected depot in the title
                                                anchor='middle'  # Center the title
                                                ),
                    width=chart_width
                )

                # Create a red dotted line at the average value
                average_opd_line = alt.Chart(pd.DataFrame({'average_opd_kms': [average_opd_kms]})).mark_rule(
                    color='red',
                    strokeDash=[5, 5]  # Dotted line
                ).encode(
                    y='average_opd_kms:Q'  # Specify the y-axis for the average line
                )

                # Combine the bar chart and the median line
                final_chart = bar_chart + average_opd_line

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
                

                
    else:
                st.error("Failed to load data.") 
    
               
    #ABSENTEEISM BY DEPOT

    # Divider for clear sectioning
    st.markdown("---")

    # Section 2: Absenteeism Baseline
    st.header("**2. Absenteeism Baseline (Absent Days/Year), FY2023-24**")

    st.markdown("""
    - **RM & DM & Doctors**: Reasons for high absenteeism should be understood
    - **Doctors**: Pay special attention to high absenteeism drivers
    - **HR**: Understand incentives (OT) and motivation
    """)
    
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
        
            # Sort data by absent_days in ascending order
            sorted_data1 = filtered_data.sort_values(by='absent_days', ascending=False)
            
            # Calculate the mean of absent days
            average_absenteeism = sorted_data1['absent_days'].mean()
        
                                        # Format the value to have no decimals and comma separators
            formatted_value = f"{int(average_absenteeism):,}"

             # Use Streamlit's markdown with custom HTML and CSS for styling
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;  /* Light grey background for a clean look */
                    padding: 20px;  /* Increased padding for better spacing */
                    border-radius: 10px;  /* Rounded corners for a modern feel */
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
                    width: 320px;  /* Slightly wider box for better readability */
                    margin: 20px auto;  /* Center the box and add top/bottom margin */
                    text-align: center;
                ">
                    <p style="
                        font-size: 14px;  /* Slightly larger text for better readability */
                        color: #333333;  /* Darker font color for contrast */
                        margin-bottom: 10px;  /* More space below the title */
                    ">
                        <strong>Absenteeism Baseline (Days/Year)</strong>
                    </p>
                    <p style="
                        font-size: 40px;  /* Larger font for the main value */
                        font-weight: bold; 
                        color: #2c3e50;  /* Darker shade for the number */
                        margin-bottom: 0;
                    ">
                        {formatted_value}
                    </p>
                </div>
                """, unsafe_allow_html=True
            )
                
            num_bars = len(sorted_data1)
            bar_width = 10  # You can adjust this value to make the bars wider or narrower
            chart_width = num_bars * bar_width
        
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                                
                # Create a bar chart using Altair with hover annotations and sorted data
                bar_chart = alt.Chart(sorted_data1).mark_bar().encode(
                    x=alt.X('employee_id', sort=None, title='Employee ID', 
                            axis=alt.Axis(ticks=False, labels=False)),  # Remove tick marks and set label angle to prevent truncation
                    y=alt.Y('absent_days', title='Total Absent Days - A+L+SL'),  # Add label for y-axis
                    tooltip=[
                                alt.Tooltip('employee_id', title='Employee ID'),  # Custom label for employee ID
                                alt.Tooltip('absent_days', title='Annual Absent Days')  # Custom label for total operational kilometers
                            ],
                    color=alt.condition(
                    alt.datum.employee_id == str(selected_employee_id),  # Condition to match the selected employee
                    alt.value('red'),  # Highlight color if condition is true
                    alt.value('steelblue')  # Default color for other bars
                    )
                    
                ).properties(
                    title=alt.TitleParams(
                                                text=f'Absenteeism by driver (Days/Year): {selected_depot}',  # Correctly display selected depot in the title
                                                anchor='middle'  # Center the title
                                                ),
                    width=chart_width
                )

                # Create a red dotted line at the average value
                average_line = alt.Chart(pd.DataFrame({'average_absenteeism': [average_absenteeism]})).mark_rule(
                    color='red',
                    strokeDash=[5, 5]  # Dotted line
                ).encode(
                    y='average_absenteeism:Q'  # Specify the y-axis for the average line
                )

                # Combine the bar chart and the average line
                final_chart = bar_chart + average_line

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 


    #PRODUCTIVITY IN HOURS

    # Divider for clear sectioning
    st.markdown("---")

    # Section 2: Absenteeism Baseline
    st.header("**3. Productivity Baseline (Hours/Year), FY2023-24**")

    st.markdown("""
    - **RM & DM**: Hours is a better measure of productivity as normalizes the different bus services like slow city routes and fast inter city services etc.
    - **RM & DM**: Check the hours calculation esp. related to multi-day interstate trips
    """)
    
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
            
            # Sort data by tot_opd_kms in ascending order
            sorted_data2 = filtered_data.sort_values(by='hours', ascending=False)
            
            # Calculate the average of hours
            average_hours = sorted_data2['hours'].mean()
        
            formatted_value = f"{int(average_hours):,}"

            # Use Streamlit's markdown with custom HTML and CSS for styling
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;  /* Light grey background for a clean look */
                    padding: 20px;  /* Increased padding for better spacing */
                    border-radius: 10px;  /* Rounded corners for a modern feel */
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
                    width: 320px;  /* Slightly wider box for better readability */
                    margin: 20px auto;  /* Center the box and add top/bottom margin */
                    text-align: center;
                ">
                    <p style="
                        font-size: 14px;  /* Slightly larger text for better readability */
                        color: #333333;  /* Darker font color for contrast */
                        margin-bottom: 10px;  /* More space below the title */
                    ">
                        <strong>Productivity Baseline (Hours/Year)</strong>
                    </p>
                    <p style="
                        font-size: 40px;  /* Larger font for the main value */
                        font-weight: bold; 
                        color: #2c3e50;  /* Darker shade for the number */
                        margin-bottom: 0;
                    ">
                        {formatted_value}
                    </p>
                </div>
                """, unsafe_allow_html=True
            )
        
            num_bars = len(sorted_data2)
            bar_width = 10  # You can adjust this value to make the bars wider or narrower
            chart_width = num_bars * bar_width
        
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                                
                # Create a bar chart using Altair with hover annotations and sorted data
                bar_chart = alt.Chart(sorted_data2).mark_bar().encode(
                    x=alt.X('employee_id', sort=None, title='Employee ID', 
                            axis=alt.Axis(ticks=False, labels=False)),  # Remove tick marks and set label angle to prevent truncation
                    y=alt.Y('hours', title='Total Hours'),  # Add label for y-axis
                    tooltip=[
                                alt.Tooltip('employee_id', title='Employee ID'),  # Custom label for employee ID
                                alt.Tooltip('hours', title='Annual Hours')  # Custom label for total operational kilometers
                            ],
                    color=alt.condition(
                    alt.datum.employee_id == str(selected_employee_id),  # Condition to match the selected employee
                    alt.value('red'),  # Highlight color if condition is true
                    alt.value('steelblue')  # Default color for other bars
                    )
                ).properties(
                                title=alt.TitleParams(
                                    text=f'Annual Productivity by Employee (Hours/Year): {selected_depot}',  # Correctly display selected depot in the title
                                    anchor='middle'  # Center the title
                                ),
                width=chart_width
                )

                # Create a red dotted line at the median value
                average_line = alt.Chart(pd.DataFrame({'average_hours': [average_hours]})).mark_rule(
                    color='red',
                    strokeDash=[5, 5]  # Dotted line
                ).encode(
                    y='average_hours:Q'  # Specify the y-axis for the median line
                )

                # Combine the bar chart and the median line
                final_chart = bar_chart + average_line

                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.")
            
                       
# PRODUCTIVITY BY HEALTH GRADE
    # Divider for clear sectioning
    st.markdown("---")

    # Section 2: Absenteeism Baseline
    st.header("**4. Productivity (Hours) + Health Grade (GHC2)**")

    st.markdown("""
    - **RM & DM**: Review under performance of drivers in good health condition
    - **Doctors**: Review the grading mechanism - clustering around 'C'
    - **Note**: Blue box indicates where middle 50% drivers productivity levels are
    - **Note**: Red circles indicate depot drivers
    - **Note**: Yellow circles indicates selected driver   
    """)   
    
    
    
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
             
            # Sort data by tot_opd_kms in ascending order
            sorted_data3 = filtered_data.dropna(subset=['final_grading']).sort_values(by='final_grading', ascending=True)
            
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data3).mark_boxplot(size=60).encode(
                    x=alt.X('final_grading:N', title='Health Grade'),
                    y=alt.Y('hours:Q', title='Annual Hours Per Driver')
                ).properties(
                    title=alt.TitleParams(
                                    text=f'Annual Hours By Health Grade (Hours/Year): {selected_depot}',  # Correctly display selected depot in the title
                                    anchor='middle'  # Center the title
                                ),
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data3).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('final_grading:N', title='Health Grade'),
                    y=alt.Y('hours:Q', title='Annual Hours Per Driver'),
                    tooltip=[
                                alt.Tooltip('employee_id', title='Employee ID'),  # Custom label for employee ID
                                alt.Tooltip('hours', title='Annual Hours')  # Custom label for total operational kilometers
                            ],
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('final_grading:N', title='Health Grade', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('hours:Q', title='Annual Hours Per Driver')
                )
                
                # Highlight the selected employee with a larger yellow dot
                highlighted_employee = alt.Chart(sorted_data3[sorted_data3['employee_id'] == str(selected_employee_id)]).mark_point(
                    color='yellow',
                    size=250, filled=True
                ).encode(
                    x=alt.X('final_grading:N', title='Health Grade'),
                    y=alt.Y('hours:Q'),
                    #tooltip=['employee_id', 'tot_opd_kms']
                )

                # Combine the box plot, swarm plot, highlighted employee point, and the custom legend
                final_chart = (box_plot + swarm_plot + highlighted_employee)
                
                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 

# DEPOT ABSENTEEISM BY HEALTH GRADE
    
    # Divider for clear sectioning
    st.markdown("---")

    # Section 2: Absenteeism Baseline
    st.header("**5. Absenteeism (Days) + Health Grade (GHC2)**")

    st.markdown("""
    - **RM & DM**: Review under performance of drivers in good health condition
    - **Doctors**: Review the grading mechanism - clustering around 'C'
    - **Note**: Blue box indicates where middle 50% drivers productivity levels are
    - **Note**: Red circles indicate depot drivers
    - **Note**: Yellow circles indicates selected driver   
    """)  
        
    
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
             
            # Sort data by tot_opd_kms in ascending order
            sorted_data3 = filtered_data.dropna(subset=['final_grading']).sort_values(by='final_grading', ascending=True)
            
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                # Create the bar graph with matplotlib
                                
                # Create a box plot
                box_plot = alt.Chart(sorted_data3).mark_boxplot(size=60).encode(
                    x=alt.X('final_grading:N', title='Health Grade'),
                    y=alt.Y('absent_days:Q', title='Annual absent days per driver')
                ).properties(
                    title=alt.TitleParams(
                                    text=f'Annual Absent Days By Health Grade (Days/Year): {selected_depot}',  # Correctly display selected depot in the title
                                    anchor='middle'  # Center the title
                                ),
                )
                
                # Create a swarm plot (jittered points)
                swarm_plot = alt.Chart(sorted_data3).mark_point(
                    color='red',
                    size=60
                ).encode(
                    x=alt.X('final_grading:N', title='Health Grade'),
                    y=alt.Y('absent_days:Q', title='Annual absent days per driver'),
                    tooltip=[
                                alt.Tooltip('employee_id', title='Employee ID'),  # Custom label for employee ID
                                alt.Tooltip('absent_days', title='Annual Absent Days')  # Custom label for total operational kilometers
                            ],
                ).transform_calculate(
                    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'  # Simulate jittering
                ).encode(
                    x=alt.X('final_grading:N', title='Health Grade', axis=alt.Axis(labelAngle=0)),
                    y=alt.Y('absent_days:Q', title='Annual absent days per driver')
                )
                
                # Highlight the selected employee with a larger yellow dot
                highlighted_employee = alt.Chart(sorted_data3[sorted_data3['employee_id'] == str(selected_employee_id)]).mark_point(
                    color='yellow',
                    size=250, filled=True
                ).encode(
                    x=alt.X('final_grading:N', title='Health Grade'),
                    y=alt.Y('absent_days:Q'),
                    #tooltip=['employee_id', 'tot_opd_kms']
                )

                # Combine the box plot, swarm plot, highlighted employee point, and the custom legend
                final_chart = (box_plot + swarm_plot + highlighted_employee)
                
                # Display the chart in Streamlit
                st.altair_chart(final_chart, use_container_width=True)
    else:
            st.error("Failed to load data.") 


    # DEPOT LEVEL DRIVER DATA

    # Divider for clear sectioning
    st.markdown("---")

    # Section 2: Absenteeism Baseline
    st.header("**6. Depot Productivity Data**")

    st.markdown("""
    - **Note**: Sort the date in the table by clicking on the header
    """)  
    
    if data is not None:
    
        # Ensure the depot column exists
        if 'depot' not in data.columns:
            st.error("Depot column not found in dataset")
        else:
             
            if filtered_data.empty:
                st.warning("No data available for the selected depot.")
            else:
                selected_columns1 = filtered_data[['employee_id','tot_opd_kms','hours','absent_days','final_grading']]
                # Display the table in Streamlit
                
                # Rename the columns for clarity and readability
                selected_columns1 = selected_columns1.rename(columns={
                    'employee_id': 'Employee ID',
                    'tot_opd_kms': 'Annual KM',
                    'hours': 'Annual Hours',
                    'absent_days': 'Annual Absent Days',
                    'final_grading': 'GHC2 Grade'
                })

                # Format numbers (e.g., Annual KM, Hours) with commas for better readability
                selected_columns1['Annual KM'] = selected_columns1['Annual KM'].apply(lambda x: f"{x:,}")
                selected_columns1['Annual Hours'] = selected_columns1['Annual Hours'].apply(lambda x: f"{x:,}")
                selected_columns1['Annual Absent Days'] = selected_columns1['Annual Absent Days'].apply(lambda x: f"{x:,}")

                # Display the table in Streamlit with a professional header
                st.write(f"### **Driver Productivity and Health Data FY 2023-24 for: {selected_depot}**")
                st.dataframe(selected_columns1.style.set_properties(**{
                    'text-align': 'center',
                    'background-color': '#f5f5f5',
                    'border': '1px solid black'
                }).set_table_styles([
                    {'selector': 'thead th', 'props': [('background-color', '#4CAF50'), ('color', 'white'), ('font-weight', 'bold')]}
                ]))
    else:
            st.error("Failed to load data.") 


def productivity_improvement_tracker():
    st.title("📊 **TGSRTC ESG Dashboard**")
    st.subheader("*HEALTH + PRODUCTIVITY*")
    st.markdown("---")  # Divider line for better sectioning
    
    # Monthly Depot Productivity (KM)
    st.header("🚍 **1. Monthly Depot Productivity (KM)**")
    st.markdown(
        """
        <div style='background-color: #f0f0f5; padding: 10px; border-radius: 10px;'>
            <p>Tracking the monthly progress of depot productivity in kilometers.</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing for visual clarity
    
    # Monthly Depot Productivity (Hours)
    st.header("🕒 **2. Monthly Depot Productivity (Hours)**")
    st.markdown(
        """
        <div style='background-color: #e6f7ff; padding: 10px; border-radius: 10px;'>
            <p>Tracking the monthly progress of depot productivity in hours.</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing
    
    # Monthly Depot Absenteeism (Days)
    st.header("🚫 **3. Monthly Depot Absenteeism (Days)**")
    st.markdown(
        """
        <div style='background-color: #ffe6e6; padding: 10px; border-radius: 10px;'>
            <p>Tracking the monthly progress of depot absenteeism in days.</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing
    
    # Monthly Driver Productivity (KM)
    st.header("🚛 **4. Monthly Driver Productivity (KM)**")
    st.markdown(
        """
        <div style='background-color: #f0f0f5; padding: 10px; border-radius: 10px;'>
            <p>Tracking the monthly progress of driver productivity in kilometers.</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing
    
    # Monthly Driver Productivity (Hours)
    st.header("🕒 **5. Monthly Driver Productivity (Hours)**")
    st.markdown(
        """
        <div style='background-color: #e6f7ff; padding: 10px; border-radius: 10px;'>
            <p>Tracking the monthly progress of driver productivity in hours.</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing
    
    # Monthly Driver Absenteeism (Days)
    st.header("🚫 **6. Monthly Driver Absenteeism (Days)**")
    st.markdown(
        """
        <div style='background-color: #ffe6e6; padding: 10px; border-radius: 10px;'>
            <p>Tracking the monthly progress of driver absenteeism in days.</p>
        </div>
        """, unsafe_allow_html=True
    )
    st.write("")  # Add spacing
    
# Productivity
if option == "STEP 1: SET BASELINE":
    depot_productivity_dashboard()  
    
elif option == "STEP 2: SET TARGETS (AI)":
    productivity_predictor()
    
elif option == "STEP 3: TRACK IMPROVEMENT":
    productivity_improvement_tracker()
