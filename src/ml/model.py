import os 
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "storage", "churn_model.joblib")

class ChurnPredictor:
    def __init__(self):
        self.model = None
        self.features = ["days_since_last_login"]
        self.load_model()
        
    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                self.model= joblib.load(MODEL_PATH)
                print("ML: Model is succesfully loaded from file")
            except:
                pass 