"""
Google Sheets Automation: Log trade signals and P&L, with trade log, summary P&L, and win ratio in separate tabs.
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from .utils.logger import setup_logger

logger = setup_logger("sheets")

# Set up Google Sheets API credentials (user must provide their own credentials JSON)
SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
CREDENTIALS_FILE = 'google_service_account.json'  # Place your credentials file in the project root


def get_gsheet_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
    client = gspread.authorize(creds)
    return client


def log_to_sheets(trade_log: pd.DataFrame, summary: pd.DataFrame, win_ratio: float, sheet_name: str = 'AlgoTradingLog'):
    try:
        client = get_gsheet_client()
        # Create or open the spreadsheet
        try:
            sheet = client.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            sheet = client.create(sheet_name)
        # Trade Log Tab
        if 'TradeLog' in [ws.title for ws in sheet.worksheets()]:
            trade_ws = sheet.worksheet('TradeLog')
            sheet.del_worksheet(trade_ws)
        trade_ws = sheet.add_worksheet(title='TradeLog', rows=str(len(trade_log)+1), cols=str(len(trade_log.columns)))
        sheet.values_update('TradeLog!A1', params={'valueInputOption': 'RAW'}, body={'values': [trade_log.columns.tolist()] + trade_log.values.tolist()})
        # Summary P&L Tab
        if 'Summary' in [ws.title for ws in sheet.worksheets()]:
            summary_ws = sheet.worksheet('Summary')
            sheet.del_worksheet(summary_ws)
        summary_ws = sheet.add_worksheet(title='Summary', rows=str(len(summary)+1), cols=str(len(summary.columns)))
        sheet.values_update('Summary!A1', params={'valueInputOption': 'RAW'}, body={'values': [summary.columns.tolist()] + summary.values.tolist()})
        # Win Ratio Tab
        if 'WinRatio' in [ws.title for ws in sheet.worksheets()]:
            win_ws = sheet.worksheet('WinRatio')
            sheet.del_worksheet(win_ws)
        win_ws = sheet.add_worksheet(title='WinRatio', rows="2", cols="2")
        sheet.values_update('WinRatio!A1', params={'valueInputOption': 'RAW'}, body={'values': [["Win Ratio", win_ratio]]})
        logger.info(f"Logged data to Google Sheets: {sheet_name}")
    except Exception as e:
        logger.error(f"Failed to log to Google Sheets: {e}")
