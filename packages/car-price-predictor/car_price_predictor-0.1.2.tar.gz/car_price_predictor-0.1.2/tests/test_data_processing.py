# tests/test_data_processing.py
import unittest
import pandas as pd
from car_price_predictor.data_processing import load_data, encode_features, scale_features

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Sample data for testing
        self.sample_data = pd.DataFrame({
            'year': [2015, 2016],
            'make': ['Kia', 'Toyota'],
            'trim': ['LX', 'SE'],
            'body': ['SUV', 'Sedan'],
            'condition': [5, 4],
            'odometer': [16639.0, 25000.0],
            'transmission': ['automatic', 'manual']
        })
    
    def test_load_data(self):
        data = load_data("../data/car_prices.csv")
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.isnull().values.any())
    
    def test_encode_features(self):
        encoded_data, label_encoders = encode_features(self.sample_data.copy())
        self.assertIsInstance(encoded_data, pd.DataFrame)
        for column in ["year", "make", "trim", "body", "condition", "odometer", "transmission"]:
            self.assertIn(column, label_encoders)
            self.assertTrue(all(isinstance(val, int) for val in encoded_data[column]))
    
    def test_scale_features(self):
        encoded_data, _ = encode_features(self.sample_data.copy())
        scaled_data, scaler = scale_features(encoded_data)
        self.assertIsInstance(scaled_data, pd.DataFrame)
        self.assertTrue((scaled_data.mean().abs() < 1e-6).all())  # Check if data is centered around 0
        self.assertTrue((scaled_data.std().round(6) == 1).all())   # Check if data is scaled

if __name__ == "__main__":
    unittest.main()
