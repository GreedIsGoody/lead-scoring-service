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
            except Exception as e:
                print(f"ML: loading error: {e} need retraining")
        else:
            print("ML: File was not found. Need initialization")
                 
                 
    def generate_mock_data(self, num_samples=500):
        
        np.random.seed(42)
        
        days_since_last_login = np.random.randint(0, 30, size=num_samples)
        support_tickets_count = np.random.randint(0,7, size=num_samples)
        total_payments = np.random.uniform(0,300,size=num_samples)
        is_premium = np.random.choice([0,1], size=num_samples, p=[0.7,0.3])
        
        df = pd.DataFrame({
            "days_since_last_login": days_since_last_login,
            "support_tickets_count": support_tickets_count,
            "total_payments": total_payments,
            "is_premium": is_premium
        })
        # Base logic churn 
        churn_risk = (
            (df["days_since_last_login"] > 15) * 0.4 +
            (df["support_tickets_count"] > 3) * 0.3 -
            (df["total_payments"]> 100) * 0.3 -
            df["is_premium"] * 0.2
        )
        df["target"] = (churn_risk + np.random.normal(0,0.1,size=num_samples) > 0.1).astype(int)
        return df
    
    def train(self, data: pd.DataFrame = None):
        #training model and saving
        if data is None:
            print("ML: Data is missing. Generate a syntetic dataset...")
            data = self.generate_mock_data()
            
        x = data[self.features]
        y = data["target"]
        
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        score = self.model.score(X_test, y_test)
        print(f"ML: Model was trained. Accurency:{score:.2f}")
        
        #Creating a storage folder and saving weight
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        print(f"ML: Model is saved in {MODEL_PATH}")
        
    def predict_churn(self, customer_features: dict) -> dict:
        if self.model is None:
            self.train()
            
        df_input = pd.DataFrame([customer_features])[self.features]
        
        prob = self.model.predict_proba(df_input)[0][1]
        
        if prob < 0.3:
            risk_level = "Low"
        elif prob < 0.7:
            risk_level= "Medium"
        else:
            risk_level = "High"
            
        return {
            "churn_probability": round(float(prob) * 100, 2),
            "risk_level": risk_level
        }
        
        
predictor = ChurnPredictor()
        