%%writefile data/data_processor.py
import pandas as pd
import numpy as np
import re
import logging
from datetime import datetime, timedelta
from .data_loader import load_usd_data, load_today_avg, load_trends_data
from utils.decorators import error_handler

logger = logging.getLogger(__name__)

@error_handler
def process_usd_data():
    try:
        # دریافت داده‌های خام
        raw_data = load_usd_data()
        
        # بررسی وجود داده
        if not raw_data or not isinstance(raw_data, list):
            logger.error("No valid USD data received")
            return pd.DataFrame(columns=['date', 'price'])
        
        # پردازش هر ردیف
        processed_rows = []
        for row in raw_data:
            try:
                # استخراج قیمت - استفاده از ستون 0 به عنوان قیمت پایانی
                price_str = re.sub(r'<.*?>', '', str(row[0])).replace(',', '')
                price = float(price_str)
                
                # استخراج تاریخ - استفاده از ستون 6
                date_str = str(row[6])
                
                # تبدیل فرمت‌های مختلف تاریخ
                for fmt in ("%Y/%m/%d", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
                    try:
                        date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # اگر هیچ فرمتی تطابق نداشت
                    logger.warning(f"Unrecognized date format: {date_str}")
                    continue
                
                processed_rows.append({'date': date, 'price': price})
                
            except Exception as e:
                logger.error(f"Error processing row: {e}\nRow content: {row}")
                continue
        
        # ایجاد DataFrame
        if not processed_rows:
            logger.error("No valid rows processed")
            return pd.DataFrame(columns=['date', 'price'])
        
        df = pd.DataFrame(processed_rows)
        
        # افزودن داده امروز
        try:
            avg = load_today_avg()
            if not np.isnan(avg):
                today = pd.to_datetime(datetime.now().date())
                df = pd.concat([
                    df,
                    pd.DataFrame([{'date': today, 'price': avg}])
                ])
        except Exception as e:
            logger.error(f"Error adding today's data: {e}")
        
        # پردازش نهایی
        df = df.drop_duplicates(subset=['date'], keep='last')
        df = df.set_index('date').sort_index()
        
        return df
    
    except Exception as e:
        logger.exception("Critical error in process_usd_data")
        return pd.DataFrame(columns=['date', 'price'])

@error_handler
def process_trends_data():
    try:
        df_long = load_trends_data()
        if df_long.empty:
            logger.warning("No trends data loaded")
            return pd.DataFrame()
        
        # تغییر نام ستون‌ها به فرمت استاندارد
        column_map = {
            'date': 'date',
            'topic': 'topic',
            'value': 'value',
            'تاریخ': 'date',
            'موضوع': 'topic',
            'مقدار': 'value'
        }
        
        # تغییر نام ستون‌ها
        df_long = df_long.rename(columns={k: v for k, v in column_map.items() if k in df_long.columns})
        
        # بررسی وجود ستون‌های الزامی
        required_columns = ['date', 'topic', 'value']
        if not all(col in df_long.columns for col in required_columns):
            logger.error("Trends data missing required columns")
            return pd.DataFrame()
        
        # تبدیل انواع داده‌ها
        df_long['date'] = pd.to_datetime(df_long['date'])
        df_long['value'] = (
            df_long['value']
            .astype(str)
            .str.replace('<1', '0.5', regex=False)
            .str.replace(',', '')
            .astype(float)
        )
        
        # تبدیل به فرمت گسترده
        df_wide = df_long.pivot_table(
            index='date', 
            columns='topic', 
            values='value', 
            aggfunc='first'
        ).ffill().bfill()
        
        return df_wide
    
    except Exception as e:
        logger.exception("Error in process_trends_data")
        return pd.DataFrame()

@error_handler
def get_full_data():
    try:
        # دریافت داده‌های دلار
        usd_df = process_usd_data()
        if usd_df.empty:
            logger.error("USD data is empty")
            return pd.DataFrame()
        
        # دریافت داده‌های روند
        trends_df = process_trends_data()
        
        # ترکیب داده‌ها
        if not trends_df.empty:
            # ادغام با حفظ تمام تاریخ‌های دلار
            full_df = usd_df.join(trends_df, how='left')
            
            # پر کردن مقادیر گمشده
            full_df = full_df.ffill().bfill()
        else:
            full_df = usd_df
        
        # فیلتر تاریخ
        cutoff = datetime.now() - timedelta(days=730)
        full_df = full_df[full_df.index >= cutoff]
        
        return full_df.dropna()
    
    except Exception as e:
        logger.exception("Error in get_full_data")
        return pd.DataFrame()
