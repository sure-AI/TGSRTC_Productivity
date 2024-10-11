import os
from TGSRTC_Productivity import logger
from TGSRTC_Productivity.entity.config_entity import ModelPredictionConfig
import pickle
import pandas as pd


class ModelPrediction:
    def __init__(self, config: ModelPredictionConfig):
        self.config = config

    def fetch_data(self):
        """Fetch data from the CSV file defined in the configuration."""
        try:
            data = pd.read_csv(self.config.data_path)  # Load data from the path in config
            return data
        except Exception as e:
            raise Exception(f"Error fetching data: {e}")

    def model_predict(self, input_data):
        """Make predictions using the trained model."""
        try:
            with open(self.config.model_path, 'rb') as file:
                model = pickle.load(file)
            prediction = model.predict(input_data)
            return prediction
        except Exception as e:
              raise e