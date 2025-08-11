import requests
import pandas as pd
import re
import os
from datetime import datetime
from config import DATA_PATHS
from utils.decorators import error_handler

@error_handler
def fetch_tgju_data():
    rev = "Gkj74Rba5CSFntmsJip7Fk5JHkUz6nxYaxGx3PPVzLowuIcXF8ufuQfMFRBs"
    url = "https://call1.tgju.org/ajax.json"
    params = {"rev": rev}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("current", {})

@error_handler
def load_usd_data():
    ts = int(datetime.now().timestamp() * 1000)
    url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/price_dollar_rl?period=all&mode=full&ts={ts}"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return res.json().get('data', [])

@error_handler
def load_today_avg():
    try:
        # دریافت داده لحظه‌ای
        data = fetch_tgju_data()
        dollar_data = data.get("price_dollar_rl", {})
        price_str = dollar_data.get("p", "").replace(",", "")
        
        if price_str:
            return float(price_str)
    except Exception:
        pass
    
    # روش جایگزین اگر دریافت لحظه‌ای شکست خورد
    try:
        params = {
            "lang": "fa",
            "draw": 1,
            "start": 0,
            "length": 30,
            "tolerance_open": 1,
            "tolerance_yesterday": 1,
            "tolerance_range": "week",
            "_": int(datetime.now().timestamp() * 1000)
        }
        
        rows = requests.get(
            "https://api.tgju.org/v1/market/indicator/today-table-data/price_dollar_rl",
            params=params, headers={'User-Agent': 'Mozilla/5.0'}
        ).json().get('data', [])
        
        prices = []
        for r in rows[:3]:
            try:
                price = int(re.sub(r'<.*?>', '', r[0]).replace(',', ''))
                prices.append(price)
            except:
                continue
        
        return sum(prices) / len(prices) if prices else float('nan')
    except Exception as e:
        print(f"Error in alternative today_avg method: {e}")
        return float('nan')

@error_handler
def load_trends_data():
    dfs = []
    for f in DATA_PATHS['trends_files']:
        file_path = os.path.join(DATA_PATHS['trends_csv'], f)
        try:
            if not os.path.exists(file_path):
                print(f"⚠️ File not found: {file_path}")
                continue
                
            df = pd.read_csv(file_path)
            
            # تطبیق نام ستون‌ها
            column_map = {
                'date': 'date',
                'topic': 'topic',
                'value': 'value',
                'نام ستون تاریخ': 'date',
                'موضوع': 'topic',
                'مقدار': 'value'
            }
            
            # تغییر نام ستون‌ها به فرمت استاندارد
            df = df.rename(columns={k: v for k, v in column_map.items() if k in df.columns})
            
            # حذف ردیف‌های با داده‌های گمشده
            df = df.dropna(subset=['date', 'topic', 'value'])
            
            dfs.append(df)
        except Exception as e:
            print(f"⚠️ Error loading {file_path}: {e}")
            continue
            
    if not dfs:
        return pd.DataFrame()
    
    combined = pd.concat(dfs, ignore_index=True)
    return combined
