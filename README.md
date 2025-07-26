# Algo-Trading System with ML & Automation

## Features
- Fetches daily stock data from Yahoo Finance for NIFTY 50 tickers
- Implements RSI < 30 + 20-DMA/50-DMA crossover strategy with 6-month backtest
- Logs trades, summary P&L, and win ratio to Google Sheets (requires service account credentials)
- ML-based prediction (Decision Tree) for next-day movement using RSI, MACD, Volume, etc.
- Telegram alerts for trade signals and error notifications (requires bot token and chat ID)
- Modular code, logging, and documentation

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Place your `google_service_account.json` in the project root for Google Sheets integration.
3. Set your Telegram bot token and chat ID in `algo_trading_system/telegram_alerts.py`.
4. Run the system from the parent directory:
   ```sh
   python -m algo_trading_system.main
   ```

## Notes
- If you see import errors, always run as a module from the parent directory.
- If you see empty trade logs, it may be due to no buy signals in the backtest period.
- For Telegram alerts, ensure your bot is added to the target chat/group.
