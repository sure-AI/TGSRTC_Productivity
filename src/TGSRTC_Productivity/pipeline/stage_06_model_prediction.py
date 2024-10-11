#import joblib 
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from TGSRTC_Productivity.config.configuration import ConfigurationManager
from TGSRTC_Productivity.components.model_prediction import ModelPrediction
from TGSRTC_Productivity import logger

STAGE_NAME = "Model Prediction"

class ModelPredictionPipeline:
    
    #def __init__(self):
    #    Open the file in read-binary mode ('rb') and load the model
    #    with open(Path('artifacts/model_trainer/model.pkl'), 'rb') as file:
    #        self.model = pickle.load(file)

    #def predict(self, data):
    #    Use the loaded model to make predictions
    #    prediction = self.model.predict(data)
    #    return prediction
    
    def __init__(self):
        self.model_prediction = None

    def load_and_fetch_data(self):
        config = ConfigurationManager()
        model_prediction_config = config.get_model_prediction_config()
        self.model_prediction = ModelPrediction(config=model_prediction_config)  # Create ModelPrediction object
        
         # Fetch data from CSV
        data = self.model_prediction.fetch_data()  # Fetch data using ModelPrediction
        return data
    
    def make_prediction(self, data):
        """Make predictions on the data."""
        prediction = self.model_prediction.model_predict(data)  # Make predictions on the data
        return prediction