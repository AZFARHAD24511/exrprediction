%%writefile config.py
import os
import random

# تنظیمات عمومی
N_LAGS = 7
TEST_SIZE = 7
ARTIFICIAL_USER_BOOST = random.randint(1751, 3987)
DOWNLOAD_CODE = os.getenv('DOWNLOAD_CODE', 'SECRET123')
API_TOKEN = os.getenv('TG_API_TOKEN')

# تنظیمات مدل
MODEL_CONFIG = {
    'RandomForest': {
        'class': 'sklearn.ensemble.RandomForestRegressor',
        'params': {'n_estimators': 100, 'random_state': 42}
    },
    'XGBoost': {
        'class': 'xgboost.XGBRegressor',
        'params': {'n_estimators': 100, 'objective': 'reg:squarederror', 'random_state': 42, 'verbosity': 0}
    }
}

# تنظیمات مسیرها - اصلاح شده برای استفاده از مسیر محلی
DATA_PATHS = {
    'trends_csv': "data",  # تغییر مسیر به دایرکتوری data/
    'trends_files': ["partial_data.csv", "partial_data_new.csv"]
}
