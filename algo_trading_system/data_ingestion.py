"""
Data ingestion module for fetching daily stock data for NIFTY 50 tickers from Yahoo Finance.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from .config import TICKERS
from .utils.logger import setup_logger

logger = setup_logger("data_ingestion")

def fetch_daily_data(tickers, period_months=6):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=period_months*30)
    all_data = {}
    for ticker in tickers:
        try:
            logger.info(f"Fetching data for {ticker} from {start_date.date()} to {end_date.date()}")
            data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval='1d')
            if not data.empty:
                all_data[ticker] = data
                logger.info(f"Fetched {len(data)} rows for {ticker}")
            else:
                logger.warning(f"No data found for {ticker}")
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
    return all_data

if __name__ == "__main__":
    data = fetch_daily_data(TICKERS)
    for ticker, df in data.items():
        print(f"{ticker}: {df.shape[0]} rows")
