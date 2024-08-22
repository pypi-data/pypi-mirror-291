from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle

def split_data(input_data, output_data, split_ratio, r_state):
    x_train, x_test, y_train, y_test = train_test_split(input_data, output_data, test_size=split_ratio, random_state=r_state)
    return x_train, x_test, y_train, y_test

def train_model(x_train, y_train, r_state, m_depth):
    rf = RandomForestRegressor(random_state=r_state, max_depth=m_depth)
    rf.fit(x_train, y_train)
    return rf

def evaluate_model(rf, x_train, y_train, x_test, y_test):
    y_train_pred = rf.predict(x_train)
    y_test_pred = rf.predict(x_test)
    train_rmse_rf = mean_squared_error(y_train, y_train_pred, squared=False)
    test_rmse_rf = mean_squared_error(y_test, y_test_pred, squared=False)
    print(f"Train RMSE: {train_rmse_rf}")
    print(f"Test RMSE: {test_rmse_rf}")
    print("R squared for train is :", rf.score(x_train, y_train) * 100)
    print("R squared for test is :", rf.score(x_test, y_test) * 100)

def save_model(rf, filename):
    with open(filename, 'wb') as file:
        pickle.dump(rf, file)
