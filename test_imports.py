# test_imports.py
print("=== Testing project imports ===")

try:
    from bot.bot_handlers import BotHandlers
    from bot.bot_runner import run_bot
    from data.data_loader import load_data
    from data.data_processor import process_data
    from model.forecasting import train_model
    from model.model_evaluation import evaluate_model
    from utils.decorators import timer
    from utils.logger import log
    from utils.plotting import plot_results

    print("✅ All modules imported successfully!")
except ImportError as e:
    print("❌ Import error:", e)
