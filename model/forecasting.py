import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.preprocessing import StandardScaler
from config import MODEL_CONFIG, N_LAGS, TEST_SIZE
from model.model_evaluation import evaluate_model
from utils.decorators import error_handler

@error_handler
def prepare_features(df, n_lags=N_LAGS):
    lagged = {}
    for lag in range(1, n_lags + 1):
        lagged[f'price_lag{lag}'] = df['price'].shift(lag)
        for kw in df.columns.drop('price'):
            lagged[f'{kw}_lag{lag}'] = df[kw].shift(lag)

    lag_df = pd.DataFrame(lagged, index=df.index).dropna()
    full_df = pd.concat([df[['price']].iloc[n_lags:], lag_df.iloc[n_lags:]], axis=1)
    return full_df, lag_df.columns.tolist()

@error_handler
def train_models(X_train, y_train):
    results = {}
    for name, config in MODEL_CONFIG.items():
        model_class = eval(config['class'])
        model = model_class(**config['params'])
        model.fit(X_train, y_train)
        results[name] = model
    return results

@error_handler
def build_next_features(base_df, features, n_lags=N_LAGS):
    next_vals = {}
    for feat in features:
        if feat.startswith('price_lag'):
            lag = int(feat.split('lag')[-1])
            next_vals[feat] = base_df['price'].iloc[-lag]
        elif '_lag' in feat:
            kw, _, lagstr = feat.rpartition('_lag')
            lag = int(lagstr)
            next_vals[feat] = base_df[kw].iloc[-lag] if kw in base_df else np.nan
        else:
            next_vals[feat] = np.nan
    return pd.DataFrame([next_vals])