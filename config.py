DATA_PATHS = {
    'usd_data': 'data/partial_data.csv',
    'today_avg': 'data/partial_data_new.csv',
    'trends': 'data/google_trends.csv'
}

models = {
    'RandomForest': {
        'class': 'RandomForestRegressor',
        'params': {
            'n_estimators': 100,
            'random_state': 42
        }
    },
    'LinearRegression': {
        'class': 'LinearRegression',
        'params': {}
    }
}
