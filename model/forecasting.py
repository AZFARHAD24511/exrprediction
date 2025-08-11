import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from utils.decorators import timer

@timer
def train_models(X_train, y_train, config):
    models = {}
    for name, params in config['models'].items():
        model_class = None
        if params['class'] == 'RandomForestRegressor':
            model_class = RandomForestRegressor
        elif params['class'] == 'LinearRegression':
            model_class = LinearRegression
        else:
            raise ValueError(f"Unknown model class: {params['class']}")
        
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
