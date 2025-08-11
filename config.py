import os

API_TOKEN = os.getenv("EXR_API_TOKEN")   # حتماً در محیط تعریف کنید
DOWNLOAD_CODE = os.getenv("DOWNLOAD_CODE", "SECRET123")

DATA_PATHS = {
    'usd_data': 'data/partial_data.csv',
    'today_avg': 'data/partial_data_new.csv',
    'trends': 'data/google_trends.csv'
}

MODEL_PARAMS = {
    'RandomForest': {'n_estimators':200, 'max_depth':8, 'min_samples_leaf':5, 'random_state':42},
    'XGBoost': {'n_estimators':200, 'max_depth':6, 'learning_rate':0.05, 'random_state':42}
}
