import pandas as pd
import os
from TGSRTC_Productivity import logger
#from sklearn.linear_model import ElasticNet
#import joblib
from TGSRTC_Productivity.entity.config_entity import ModelTrainerConfig
#from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pickle



class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    
    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)


        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]


        rf = RandomForestClassifier()
        rf.fit(train_x, train_y.values.ravel())

        with open(os.path.join(self.config.root_dir, self.config.model_name), 'wb') as file:
            pickle.dump(rf, file)
        #joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))