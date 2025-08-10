import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
from utils.decorators import error_handler


@error_handler
def plot_forecast_farsi(dates, actual, next_date, pred, model_name):
    title  = get_display(arabic_reshaper.reshape(f'پیش‌بینی نرخ دلار برای {next_date.date().isoformat()}'))
    lbl_rt = get_display(arabic_reshaper.reshape('قیمت واقعی'))
    lbl_pr = get_display(arabic_reshaper.reshape(f'پیش‌بینی (مدل {model_name})'))
    xl     = get_display(arabic_reshaper.reshape('تاریخ'))
    yl     = get_display(arabic_reshaper.reshape('قیمت دلار آزاد (ریال)'))

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(dates, actual, label=lbl_rt)
    ax.scatter([next_date], [pred], label=lbl_pr, marker='o', color='red')
    ax.set_title(title)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.legend()
    ax.grid(True)
    ax.tick_params(axis='x', rotation=90)
    plt.tight_layout()
    return fig
