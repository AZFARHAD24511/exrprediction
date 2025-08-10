import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data.data_processor import get_full_data
from model.forecasting import prepare_features, train_models, build_next_features
from model.model_evaluation import evaluate_model
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os

def main():
    # 1. دریافت و پردازش داده‌ها
    print("🔍 در حال دریافت و پردازش داده‌ها...")
    df = get_full_data()
    
    if df.empty:
        print("❌ خطا: داده‌ای یافت نشد. لطفاً مسیر فایل‌های CSV را بررسی کنید.")
        return
        
    print(f"✅ داده‌ها با موفقیت بارگیری شدند. تعداد رکوردها: {len(df)}")
    print(f"آخرین تاریخ موجود: {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"آخرین قیمت ثبت شده: {df['price'].iloc[-1]:,.0f} ریال")
    
    # 2. آماده‌سازی ویژگی‌ها
    print("\n🔧 در حال آماده‌سازی ویژگی‌ها...")
    full_df, features = prepare_features(df)
    
    if full_df.empty:
        print("❌ خطا: ویژگی‌ها به درستی ایجاد نشدند.")
        return
        
    print(f"ویژگی‌های ایجاد شده: {len(features)}")
    print("نمونه ویژگی‌ها:", features[:5])
    
    # 3. آموزش مدل‌ها
    print("\n🤖 در حال آموزش مدل‌ها...")
    X = full_df[features]
    y = full_df['price']
    
    test_size = min(7, len(X) // 3)
    X_train, X_test = X[:-test_size], X[-test_size:]
    y_train, y_test = y[:-test_size], y[-test_size:]
    
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    
    models = train_models(X_train_s, y_train)
    
    # 4. ارزیابی مدل‌ها
    print("\n📊 ارزیابی مدل‌ها:")
    results = {}
    for name, model in models.items():
        results[name] = evaluate_model(model, X_test_s, y_test)
        print(f"\nمدل {name}:")
        print(f"  RMSE: {results[name]['rmse']:.2f}")
        print(f"  MAPE: {results[name]['mape']:.2f}%")
    
    # 5. پیش‌بینی روز بعد
    best_name = min(results, key=lambda k: results[k]['rmse'])
    print(f"\n🏆 مدل منتخب: {best_name}")
    
    next_features = build_next_features(df, features)
    next_scaled = scaler.transform(next_features)
    prediction = models[best_name].predict(next_scaled)[0]
    
    next_date = df.index[-1] + timedelta(days=1)
    print(f"\n🔮 پیش‌بینی قیمت دلار برای {next_date.strftime('%Y-%m-%d')}:")
    print(f"  {prediction:,.0f} ریال")
    
    # 6. تولید نمودار (اختیاری)
    plt.figure(figsize=(10, 5))
    plt.plot(df.index[-30:], df['price'].values[-30:], label='قیمت واقعی')
    plt.axvline(x=df.index[-1], color='r', linestyle='--', alpha=0.5)
    plt.annotate(f'پیش‌بینی: {prediction:,.0f}', 
                 (next_date, prediction),
                 xytext=(next_date + timedelta(days=2), prediction),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    plt.title(f'پیش‌بینی قیمت دلار - {next_date.strftime("%Y-%m-%d")}')
    plt.xlabel('تاریخ')
    plt.ylabel('قیمت (ریال)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # ذخیره نمودار
    os.makedirs('output', exist_ok=True)
    plot_path = f'output/forecast_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(plot_path)
    print(f"\n📈 نمودار پیش‌بینی در مسیر زیر ذخیره شد:\n{os.path.abspath(plot_path)}")

if __name__ == "__main__":
    main()
