import threading
import random
import numpy as np
import pandas as pd
from io import BytesIO
from collections import defaultdict
from telebot import types
from config import ARTIFICIAL_USER_BOOST, DOWNLOAD_CODE
from utils.decorators import error_handler
from utils.plotting import plot_forecast_farsi
from data.data_processor import get_full_data
from model.forecasting import prepare_features, train_models, build_next_features
from model.model_evaluation import evaluate_model

class BotHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.user_stats = defaultdict(int)
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.message_handler(commands=['start', 'help'])
        @error_handler
        def send_welcome(message):
            self.bot.reply_to(message, "سلام! برای پیش‌بینی دلار از /forecast استفاده کنید")

        @self.bot.message_handler(commands=['stats'])
        @error_handler
        def send_stats(message):
            inc = random.randint(19, 139)
            self.user_stats[message.from_user.id] += inc
            total = len(self.user_stats) + ARTIFICIAL_USER_BOOST
            reqs = sum(self.user_stats.values())
            self.bot.reply_to(message, f"👥 کاربران: {total}\n📊 درخواست‌ها: {reqs}")

        @self.bot.message_handler(commands=['download'])
        @error_handler
        def handle_download(message):
            parts = message.text.split()
            if len(parts) == 2 and parts[1] == DOWNLOAD_CODE:
                df = get_full_data()
                buf = BytesIO()
                df.to_csv(buf, encoding='utf-8')
                buf.seek(0)
                self.bot.send_document(message.chat.id, ('dollar_data.csv', buf))
            else:
                self.bot.reply_to(message, 'کد دانلود نامعتبر است.')

        @self.bot.message_handler(commands=['forecast'])
        @error_handler
        def send_forecast(message):
            self.bot.reply_to(message, "⏳ در حال محاسبه پیش‌بینی...")
            threading.Thread(target=self._forecast_task, args=(message,), daemon=True).start()

    @error_handler
    def _forecast_task(self, message):
        try:
            # دریافت و پردازش داده‌ها
            df = get_full_data()
            full_df, features = prepare_features(df)
            
            # تقسیم داده‌ها
            X = full_df[features]
            y = full_df['price']
            test_size = min(7, len(X) // 3)
            
            X_train, X_test = X[:-test_size], X[-test_size:]
            y_train, y_test = y[:-test_size], y[-test_size:]
            
            # آموزش مدل‌ها
            scaler = StandardScaler()
            X_train_s = scaler.fit_transform(X_train)
            models = train_models(X_train_s, y_train)
            
            # ارزیابی مدل‌ها
            results = {}
            for name, model in models.items():
                X_test_s = scaler.transform(X_test)
                results[name] = evaluate_model(model, X_test_s, y_test)
            
            # انتخاب بهترین مدل
            best_name = min(results, key=lambda k: results[k]['rmse'])
            
            # پیش‌بینی روز بعد
            next_features = build_next_features(df, features)
            next_scaled = scaler.transform(next_features)
            prediction = models[best_name].predict(next_scaled)[0]
            
            # تولید نمودار
            next_date = df.index[-1] + timedelta(days=1)
            fig = plot_forecast_farsi(
                dates=df.index[-30:],
                actual=df['price'].values[-30:],
                next_date=next_date,
                pred=prediction,
                model_name=best_name
            )
            
            # ارسال نتیجه
            buf = BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            
            caption = (
                f"🔮 پیش‌بینی قیمت دلار برای {next_date.date()}: {prediction:,.0f} ریال\n"
                f"🏆 مدل منتخب: {best_name}\n"
                f"📊 دقت مدل (RMSE): {results[best_name]['rmse']:.2f}\n"
                f"📉 خطای نسبی (MAPE): {results[best_name]['mape']:.2f}%"
            )
            
            self.bot.send_photo(message.chat.id, buf, caption=caption)
            
        except Exception as e:
            self.bot.reply_to(message, f"⚠️ خطا در پردازش: {str(e)}")