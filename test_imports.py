print("=== Testing project imports ===")

try:
    from bot.bot_handlers import BotHandlers  # به جای handle_message
    from bot.bot_runner import BotRunner     # به جای run_bot
    from data.data_processor import get_full_data  # توجه به نام تو کد شما
    from model.forecasting import prepare_features, train_models, build_next_features
    from model.model_evaluation import evaluate_model
    from utils.decorators import error_handler
    from utils.logger import setup_logger
    from utils.plotting import plot_forecast_farsi

    print("✅ All modules imported successfully!")
except ImportError as e:
    print("❌ Import error:", e)
