import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score

def safe_mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    if not mask.any(): return np.nan
    return np.mean(np.abs((y_true[mask]-y_pred[mask])/y_true[mask]))*100

def train_and_select(full_df, features, test_size=7, cv_splits=5, rf_params=None, xgb_params=None):
    # ... (همان منطق شما؛ فقط به شکل تابع ماژوله شده)
    # بازگرداندن دیکشنری شامل model, model_name, rmse, r2, mape, pred_next, predict_date
    pass
