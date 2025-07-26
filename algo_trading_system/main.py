"""
Main entry point for Algo-Trading System with ML & Automation
"""
from algo_trading_system.data_ingestion import fetch_daily_data
from algo_trading_system.config import TICKERS
from algo_trading_system.strategy import backtest
from algo_trading_system.ml_model import run_ml_on_data
from algo_trading_system.sheets import log_to_sheets
from algo_trading_system.telegram_alerts import send_telegram_message
import pandas as pd

def auto_run():
    try:
        # 1. Fetch data
        data = fetch_daily_data(TICKERS)
        # 2. Run strategy and backtest
        backtest_results = backtest(data)
        # 3. Prepare trade log and summary
        trade_log = []
        for ticker, signals in backtest_results.items():
            for idx, row in signals.iterrows():
                trade_log.append({
                    'Ticker': ticker,
                    'Date': idx.strftime('%Y-%m-%d'),
                    'Close': row['Close'],
                    'RSI': row['RSI'],
                    '20DMA': row['20DMA'],
                    '50DMA': row['50DMA']
                })
        trade_log_df = pd.DataFrame(trade_log)
        # 4. Calculate summary P&L and win ratio (placeholder logic)
        summary = trade_log_df.groupby('Ticker').agg({'Close': ['count', 'mean']})
        win_ratio = 0.0
        if not trade_log_df.empty:
            win_ratio = (trade_log_df['Close'].diff().fillna(0) > 0).sum() / len(trade_log_df)
        # 5. Log to Google Sheets
        log_to_sheets(trade_log_df, summary, win_ratio)
        # 6. Run ML model
        ml_results = run_ml_on_data(data)
        print("ML Prediction Accuracy:", ml_results)
        # 7. Send Telegram alert for new signals
        if not trade_log_df.empty:
            send_telegram_message(f"New trade signals generated: {len(trade_log_df)} signals. Win ratio: {win_ratio:.2%}")
    except Exception as e:
        send_telegram_message(f"Algo-Trading System Error: {e}")
        raise

if __name__ == "__main__":
    auto_run()
