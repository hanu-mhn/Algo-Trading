"""
Trading strategy module: Implements RSI < 30 as a buy signal, confirmed by 20-DMA crossing above 50-DMA. Includes backtesting for 6 months.
"""
import pandas as pd
import numpy as np
from .utils.logger import setup_logger

logger = setup_logger("strategy")

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def moving_average(series, window):
    return series.rolling(window=window).mean()

def generate_signals(df):
    df = df.copy()
    df['RSI'] = calculate_rsi(df['Close'])
    df['20DMA'] = moving_average(df['Close'], 20)
    df['50DMA'] = moving_average(df['Close'], 50)
    df['Buy'] = False
    for i in range(1, len(df)):
        if (
            df['RSI'].iloc[i] < 30 and
            df['20DMA'].iloc[i-1] <= df['50DMA'].iloc[i-1] and
            df['20DMA'].iloc[i] > df['50DMA'].iloc[i]
        ):
            df.at[df.index[i], 'Buy'] = True
    return df

def backtest(data_dict):
    results = {}
    for ticker, df in data_dict.items():
        logger.info(f"Backtesting {ticker}")
        signals = generate_signals(df)
        buy_signals = signals[signals['Buy']]
        results[ticker] = buy_signals[['Close', 'RSI', '20DMA', '50DMA']]
        logger.info(f"{len(buy_signals)} buy signals for {ticker}")
    return results

if __name__ == "__main__":
    from .data_ingestion import fetch_daily_data
    from .config import TICKERS
    data = fetch_daily_data(TICKERS)
    backtest_results = backtest(data)
    for ticker, signals in backtest_results.items():
        print(f"{ticker}: {len(signals)} buy signals")
