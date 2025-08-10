%%writefile data/data_processor.py
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from .data_loader import load_usd_data, load_today_avg, load_trends_data
from utils.decorators import error_handler

@error_handler
def process_usd_data():
    rows = load_usd_data()
    rec = []
    
    if not rows:
        print("⚠️ No data received from API")
        return pd.DataFrame()
    
    for row in rows:
        try:
            # استفاده از قیمت بسته (close price) - ستون 3
            price_str = re.sub(r'<.*?>', '', row[3]).replace(',', '')
            price = float(price_str)
            
            # تاریخ در ستون 6 به فرمت YYYY/MM/DD
            date_str = row[6]
            date = datetime.strptime(date_str, "%Y/%m/%d")
            
            rec.append({'date': date, 'price': price})
        except Exception as e:
            print(f"⚠️ Error processing row: {e}")
            continue
    
    if not rec:
        return pd.DataFrame()
    
    df = pd.DataFrame(rec).set_index('date').sort_index()
    
    # افزودن داده امروز
    avg = load_today_avg()
    today = pd.to_datetime(datetime.now().date())
    
    if not np.isnan(avg):
        df.loc[today] = avg
    
    return df[~df.index.duplicated(keep='last')].sort_index()

@error_handler
def process_trends_data():
    df_long = load_trends_data()
    if df_long.empty:
        print("⚠️ No trends data loaded")
        return pd.DataFrame()
    
    # اطمینان از وجود ستون‌های مورد نیاز
    required_columns = ['date', 'topic', 'value']
    if not all(col in df_long.columns for col in required_columns):
        print("⚠️ Trends data missing required columns")
        return pd.DataFrame()
    
    # تبدیل تاریخ و مقدار
    try:
        df_long['date'] = pd.to_datetime(df_long['date'])
        df_long['value'] = df_long['value'].astype(str).str.replace('<1', '0.5').astype(float)
    except Exception as e:
        print(f"⚠️ Error processing trends data: {e}")
        return pd.DataFrame()
    
    return df_long.pivot(index='date', columns='topic', values='value').ffill().bfill()

@error_handler
def get_full_data():
    usd = process_usd_data()
    
    if usd.empty:
        print("⚠️ USD data is empty")
        return pd.DataFrame()
    
    cutoff = datetime.now() - timedelta(days=730)
    usd = usd[usd.index >= cutoff]
    
    trends = process_trends_data()
    
    if trends.empty:
        print("⚠️ Using USD data only (no trends)")
        return usd
    
    # مطابقت دادن تاریخ‌های دو دیتافریم
    merged = usd.join(trends, how='left')
    
    # پر کردن مقادیر گمشده
    merged = merged.ffill().bfill().dropna()
    
    return merged
