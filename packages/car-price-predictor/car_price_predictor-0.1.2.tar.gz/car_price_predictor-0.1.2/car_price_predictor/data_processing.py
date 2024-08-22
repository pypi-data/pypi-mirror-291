import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

def load_data(file_path):
    dataset = pd.read_csv(file_path)
    dataset.dropna(axis=0, inplace=True)
    return dataset

def encode_features(dataset):
    label_encoders = {}
    for column in ["year", "make", "trim", "body", "condition", "odometer", "transmission"]:
        le = LabelEncoder()
        dataset[column] = le.fit_transform(dataset[column])
        label_encoders[column] = le
    return dataset, label_encoders

def scale_features(input_data):
    scaler = StandardScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(input_data), columns=input_data.columns)
    return scaled_data, scaler

def save_encoders_and_scaler(label_encoders, scaler, encoders_path, scalar_path):
    for column, le in label_encoders.items():
        with open(f"{encoders_path}{column}_le.pkl", 'wb') as file:
            pickle.dump(le, file)
    with open(f"{scalar_path}scaler.pkl", 'wb') as file:
        pickle.dump(scaler, file)
