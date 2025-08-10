import requests
import pandas as pd
import re
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
    try:
        rows = requests.get(
            "https://api.tgju.org/v1/market/indicator/today-table-data/price_dollar_rl",
            params=params, headers={'User-Agent': 'Mozilla/5.0'}
        ).json().get('data', [])
        prices = [int(re.sub(r'<.*?>', '', r[0]).replace(',', '')) for r in rows[:3]]
        return sum(prices) / len(prices) if prices else float('nan')
    except Exception:
        return float('nan')

@error_handler
def load_trends_data():
    dfs = []
    for f in DATA_PATHS['trends_files']:
        file_path = os.path.join(DATA_PATHS['trends_csv'], f)
        try:
            if not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path, parse_dates=['date'])
            df['value'] = df['value'].astype(str).str.replace('<1', '0.5', regex=False).astype(float)
            dfs.append(df)
        except Exception:
            continue
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()