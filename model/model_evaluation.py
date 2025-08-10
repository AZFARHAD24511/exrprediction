import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

@error_handler
def safe_mape(y_true, y_pred):
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    denom = np.where(y_true == 0, np.nan, y_true)
    return np.nanmean(np.abs((y_true - y_pred) / denom)) * 100

@error_handler
def evaluate_model(model, X_test, y_test):
    pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred) if len(y_test) > 1 else float('nan')
    mape = safe_mape(y_test, pred)
    return {
        'rmse': rmse,
        'r2': r2,
        'mape': mape,
        'predictions': pred
    }