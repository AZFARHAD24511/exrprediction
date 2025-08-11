import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from utils.decorators import timer
# دیکشنری نگاشت نام کلاس به کلاس پایتون
MODEL_MAP = {
    'RandomForestRegressor': RandomForestRegressor,
    'LinearRegression': LinearRegression
}

@timer
def train_models(X_train, y_train, config):
    models = {}
    for name, params in config['models'].items():
        model_name = params['class']
        if model_name not in MODEL_MAP:
            raise ValueError(f"Unknown model class: {model_name}")
        model_class = MODEL_MAP[model_name]
        model = model_class(**params.get('params', {}))
        model.fit(X_train, y_train)
        models[name] = model
    return models

@timer
def evaluate_models(models, X_test, y_test):
    results = {}
    for name, model in models.items():
        preds = model.predict(X_test)
        mse = np.mean((preds - y_test) ** 2)
        results[name] = {'mse': mse}
    return results

@timer
def predict(models, X):
    predictions = {}
    for name, model in models.items():
        predictions[name] = model.predict(X)
    return predictions
