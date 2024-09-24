import os
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

        data = data[[#'employee_id',
                 'age', 
                 'depot',
                 #'absent_days', 
                 'tot_opd_kms', 
                 #'hours',
                 #'tot_schedules', 
                 #'palle_schedules', 
                 #'suplux_schedules',
                 #'express_schedules',
                 #'day_schedules',
                 #'night_schedules',
                 #'bus_age_0to5',
                 #'bus_age_5to10',
                 #'bus_age_above10', 
                 #'bus_kms_0to5l', 
                 #'bus_kms_5to10l',
                 #'bus_kms_above10l', 
                 'creatinine_value', 
                 #'creatinine_interpret',
                 #'blood_pressure_systolic', 
                 'blood_pressure_diastolic',
                 #'blood_pressure_interpret', 
                 #'hemoglobin_value', 
                 #'hemoglobin_interpret',
                 'glucose_random_value', 
                 #'glucose_interpret', 
                 'bilirubin_value',
                 #'bilirubin_interpret', 
                 'total_cholestrol', 
                 #'final_grading', 
                 #'PERF',
                 #'ECG_interpret', 
                 #'BMI', 
                 #'alcohol', 
                 #'smoke', 
                 #'tobacco'
                ]]
        
        # One-hot encode the 'depot' column
        data = pd.get_dummies(data, columns=['depot'], drop_first=False)
        
        # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)
        