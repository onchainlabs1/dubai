"""Lightweight online regressor for occupancy prediction."""
from river import linear_model, preprocessing

class OnlineOccupancyRegressor:
    def __init__(self):
        self.model = preprocessing.StandardScaler() | linear_model.LinearRegression()

    def predict(self, features: dict) -> float:
        y = self.model.predict_one(features) or 0.8
        return max(0.0, min(1.0, y))

    def learn(self, features: dict, target: float):
        self.model.learn_one(features, target)