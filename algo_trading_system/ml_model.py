"""
ML Automation: Predict next-day movement using RSI, MACD, Volume, etc. Outputs prediction accuracy.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from .strategy import calculate_rsi, moving_average
from .utils.logger import setup_logger

logger = setup_logger("ml_model")

def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def prepare_features(df):
    df = df.copy()
    df['RSI'] = calculate_rsi(df['Close'])
    df['MACD'], df['MACD_signal'] = calculate_macd(df['Close'])
    df['20DMA'] = moving_average(df['Close'], 20)
    df['50DMA'] = moving_average(df['Close'], 50)
    df['Return'] = df['Close'].pct_change()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)  # 1 if next day up, else 0
    df = df.dropna()
    features = ['RSI', 'MACD', 'MACD_signal', '20DMA', '50DMA', 'Volume', 'Return']
    return df[features], df['Target']

def train_predict_model(df):
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    logger.info(f"Prediction accuracy: {accuracy:.2%}")
    return model, accuracy

def run_ml_on_data(data_dict):
    results = {}
    for ticker, df in data_dict.items():
        logger.info(f"Training ML model for {ticker}")
        try:
            model, accuracy = train_predict_model(df)
            results[ticker] = accuracy
        except Exception as e:
            logger.error(f"ML model failed for {ticker}: {e}")
            results[ticker] = None
    return results

if __name__ == "__main__":
    from .data_ingestion import fetch_daily_data
    from .config import TICKERS
    data = fetch_daily_data(TICKERS)
    acc = run_ml_on_data(data)
    for ticker, accuracy in acc.items():
        print(f"{ticker}: {accuracy if accuracy is not None else 'N/A'} accuracy")
