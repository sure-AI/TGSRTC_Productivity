import os
import numpy as np
from TGSRTC_Productivity import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from TGSRTC_Productivity.entity.config_entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    
    ## Note: You can add different data transformation techniques such as Scaler, PCA and all
    #You can perform all kinds of EDA in ML cycle here before passing this data to the model

    # I am only adding train_test_spliting cz this data is already cleaned up


    def train_test_spliting(self):
        data = pd.read_csv(self.config.data_path)

        # Select rows where the createnine_value is not null
        data = data[data['creatinine_value'].notnull()]

        data = data[[#'employee_id',
                    'age', 
                    'depot',
                    #'absent_days', 
                    #'tot_opd_kms', 
                    'hours',
                    'tot_schedules', 
                    'palle_schedules', 
                    #'suplux_schedules',
                    #'express_schedules',
                    'cityord_schedules',
                    'metroexp_schedules',
                    #'day_schedules',
                    'night_schedules',
                    #'bus_age_0to5',
                    #'bus_age_5to10',
                    #'bus_age_above10', 
                    #'bus_kms_0to5l', 
                    #'bus_kms_5to10l',
                    #'bus_kms_above10l', 
                    #'creatinine_value', 
                    'creatinine_interpret',
                    #'blood_pressure_systolic', 
                    #'blood_pressure_diastolic',
                    'blood_pressure_interpret', 
                    #'hemoglobin_value', 
                    #'hemoglobin_interpret',
                    #'glucose_random_value', 
                    'glucose_interpret', 
                    #'bilirubin_value',
                    'bilirubin_interpret', 
                    #'total_cholestrol', 
                    'cholestrol_interpret', 
                    #'final_grading', 
                    #'PERF',
                    'ECG_interpret', 
                    #'BMI', 
                    #'alcohol', 
                    #'smoke', 
                    #'tobacco'
                    ]]
                
        # Update 'ECG_Interpret' where its value is not 'Within Normal Limits'
        data.loc[data['ECG_interpret'] != 'Within Normal Limits', 'ECG_interpret'] = 'Abnormal'
    
        # One-hot encode the string columns
        data = pd.get_dummies(data, 
                                columns=[
                                'depot',
                                'creatinine_interpret', 
                                'blood_pressure_interpret', 
                                'glucose_interpret', 
                                'bilirubin_interpret', 
                                'cholestrol_interpret',
                                'ECG_interpret'
                                ], 
                                drop_first=True)
        
        hour_bins = [0, 1000, 2000, 3000, float('inf')]
        hour_labels = [0, 1, 2, 3]

        # Create a new column 'hours' with categorized values
        data['hours_category'] = pd.cut(data['hours'], 
                                    hour_bins, 
                                    labels=hour_labels, 
                                    right=False)
        
        data['night_percent'] = np.where(data['tot_schedules'] != 0, 
                                    (data['night_schedules'] / data['tot_schedules']) * 100, 
                                    0)
        
        data['palle_percent'] = np.where(data['tot_schedules'] != 0, 
                                    (data['palle_schedules'] / data['tot_schedules']) * 100, 
                                    0)
        
        data['cityord_percent'] = np.where(data['tot_schedules'] != 0, 
                                    (data['cityord_schedules'] / data['tot_schedules']) * 100, 
                                    0)
    
        data['metroexp_percent'] = np.where(data['tot_schedules'] != 0, 
                                    (data['metroexp_schedules'] / data['tot_schedules']) * 100, 
                                    0)
        
        data = data.drop([
                            'hours',
                            'tot_schedules', 
                            'night_schedules', 
                            'palle_schedules',
                            'cityord_schedules',
                            'metroexp_schedules',
                        ], 
                        axis=1)
        
        # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)
        