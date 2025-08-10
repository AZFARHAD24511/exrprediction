import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from .data_loader import load_usd_data, load_today_avg, load_trends_data
from utils.decorators import error_handler

@error_handler
def process_usd_data():
    rows = load_usd_data()
    rec = []
    for row in rows:
        try:
            price = float(re.sub(r'<.*?>', '', row[0]).replace(',', ''))
            date = datetime.strptime(row[6], "%Y/%m/%d")
            rec.append({'date': date, 'price': price})
        except Exception:
            continue
    df = pd.DataFrame(rec).set_index('date').sort_index()
    
    avg = load_today_avg()
    today = pd.to_datetime(datetime.now().date())
    if not np.isnan(avg):
        df.loc[today] = avg
    
    return df[~df.index.duplicated(keep='last')].sort_index()

@error_handler
def process_trends_data():
    df_long = load_trends_data()
    if df_long.empty:
        return pd.DataFrame()
    return df_long.pivot(index='date', columns='topic', values='value').ffill().bfill().infer_objects()

@error_handler
def get_full_data():
    usd = process_usd_data()
    cutoff = datetime.now() - timedelta(days=730)
    usd = usd[usd.index >= cutoff]
    trends = process_trends_data().reindex(usd.index).ffill().bfill()
    return usd.join(trends).dropna()