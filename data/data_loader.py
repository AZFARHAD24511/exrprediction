import re
import requests
import pandas as pd
from datetime import datetime

def load_usd_data():
    ts = int(datetime.now().timestamp() * 1000)
    url = f"https://api.tgju.org/v1/market/indicator/summary-table-data/price_dollar_rl?period=all&mode=full&ts={ts}"
    res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    rows = res.json().get('data', [])
    rec = []
    for row in rows:
        try:
            price = float(re.sub(r'<.*?>','', row[0]).replace(',',''))
            date = datetime.strptime(row[6], "%Y/%m/%d")
            rec.append({'date': date, 'price': price})
        except:
            continue
    df = pd.DataFrame(rec).set_index('date').sort_index()
    return df

# مشابه توابع load_today_avg, load_trends_csv ...
