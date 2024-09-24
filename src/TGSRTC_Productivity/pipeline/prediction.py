#import joblib 
import pickle
import numpy as np
import pandas as pd
from pathlib import Path


class PredictionPipeline:
    def __init__(self):
        # Open the file in read-binary mode ('rb') and load the model
        with open(Path('artifacts/model_trainer/model.pkl'), 'rb') as file:
            self.model = pickle.load(file)

    def predict(self, data):
        # Use the loaded model to make predictions
        prediction = self.model.predict(data)
        return prediction