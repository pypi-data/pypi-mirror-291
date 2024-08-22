# tests/test_model_training.py
import unittest
import pandas as pd
from car_price_predictor.model_training import split_data, train_model, evaluate_model
from car_price_predictor.data_processing import encode_features, scale_features

class TestModelTraining(unittest.TestCase):

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
        self.sample_target = pd.DataFrame({
            'sellingprice': [15000, 16000],
            'hourly': [100, 120],
            'daily': [300, 320],
            'weekly': [1000, 1050],
            'monthly': [3000, 3100]
        })
        self.encoded_data, _ = encode_features(self.sample_data.copy())
        self.scaled_data, _ = scale_features(self.encoded_data)

    def test_split_data(self):
        x_train, x_test, y_train, y_test = split_data(self.scaled_data, self.sample_target)
        self.assertEqual(x_train.shape[0], 1)
        self.assertEqual(x_test.shape[0], 1)
        self.assertEqual(y_train.shape[0], 1)
        self.assertEqual(y_test.shape[0], 1)
    
    def test_train_model(self):
        x_train, x_test, y_train, y_test = split_data(self.scaled_data, self.sample_target)
        model = train_model(x_train, y_train)
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, "predict"))
    
    def test_evaluate_model(self):
        x_train, x_test, y_train, y_test = split_data(self.scaled_data, self.sample_target)
        model = train_model(x_train, y_train)
        evaluate_model(model, x_train, y_train, x_test, y_test)
        # The evaluation prints results; you can check if no exceptions are raised during the process

if __name__ == "__main__":
    unittest.main()
