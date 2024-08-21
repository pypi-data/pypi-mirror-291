import pandas as pd
import joblib


def load_model(model_path):
    return joblib.load(model_path)

def load_encoders_and_scaler(encoders_path,scalar_path):
    encoders = {}
    for column in ["year", "make", "trim", "body", "condition", "transmission"]:
        encoders[column] = joblib.load(f"{encoders_path}{column}_le.joblib")
    scaler = joblib.load(f"{scalar_path}scaler.joblib")
    return encoders, scaler

def preprocess_new_data(new_data, encoders, scaler):
    for column, le in encoders.items():
        new_data[column] = le.transform([new_data[column]])[0]
    new_data_df = pd.DataFrame([new_data])
    new_data_standardized = pd.DataFrame(scaler.transform(new_data_df), columns=new_data_df.columns)
    return new_data_standardized

def predict_price(model, new_data_standardized):
    return model.predict(new_data_standardized)
