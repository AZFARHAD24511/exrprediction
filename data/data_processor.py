import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .data_loader import load_usd_data, load_trends_csv

def prepare_full_df(n_lags=7, lookback_days=730):
    usd = load_usd_data()
    cutoff = datetime.now() - timedelta(days=lookback_days)
    usd = usd[usd.index >= cutoff]
    trends = load_trends_csv().reindex(usd.index).ffill().bfill()
    df = usd.join(trends).dropna(how='all')

    pieces = []
    for lag in range(0, n_lags+1):
        suffix = 'today' if lag==0 else f'lag{lag}'
        pieces.append(df['price'].shift(lag).rename(f'price_{suffix}'))

    if trends is not None and not trends.empty:
        for col in trends.columns:
            for lag in range(0, n_lags+1):
                suffix = 'today' if lag==0 else f'lag{lag}'
                pieces.append(df[col].shift(lag).rename(f'{col}_{suffix}'))

    feat_df = pd.concat(pieces, axis=1)
    target = df['price'].shift(-1).rename('target')
    full_df = pd.concat([feat_df, df[['price']].rename(columns={'price':'price_raw'}), target], axis=1).dropna(axis=0, how='all').copy()
    features = [c for c in full_df.columns if c not in ('price_raw','target')]
    return full_df, features
