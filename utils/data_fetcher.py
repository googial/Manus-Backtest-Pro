import os
import pandas as pd
import yfinance as yf
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

def fetch_crypto_data(symbol, timeframe_str, days=730):
    """Fetch crypto data from Alpaca."""
    client = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    if timeframe_str == "1h":
        tf = TimeFrame.Hour
    elif timeframe_str == "4h":
        tf = TimeFrame(4, TimeFrame.Hour.unit)
    else:
        raise ValueError("Unsupported timeframe. Use '1h' or '4h'.")
        
    request_params = CryptoBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=tf,
        start=start_date,
        end=end_date
    )
    
    bars = client.get_crypto_bars(request_params)
    df = bars.df.reset_index()
    # Ensure consistent column names
    df = df.rename(columns={'timestamp': 'datetime'})
    return df

def fetch_nifty_data(timeframe_str, days=730):
    """Fetch Nifty 50 data from Yahoo Finance."""
    # Nifty 50 symbol on Yahoo Finance is ^NSEI
    symbol = "^NSEI"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    interval = "1h" if timeframe_str == "1h" else "1h" # yfinance doesn't have 4h, we'll resample
    
    df = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    
    if timeframe_str == "4h":
        # Resample 1h to 4h
        df = df.resample('4H').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
        
    df = df.reset_index()
    df = df.rename(columns={
        'Datetime': 'datetime',
        'Date': 'datetime',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    })
    return df

def download_all_data():
    assets = {
        "BTC/USD": "crypto",
        "ETH/USD": "crypto",
        "SOL/USD": "crypto",
        "NIFTY": "stock"
    }
    timeframes = ["1h", "4h"]
    
    os.makedirs("data", exist_ok=True)
    
    for symbol, asset_type in assets.items():
        for tf in timeframes:
            print(f"Fetching {symbol} {tf}...")
            try:
                if asset_type == "crypto":
                    df = fetch_crypto_data(symbol, tf)
                else:
                    df = fetch_nifty_data(tf)
                
                filename = f"data/{symbol.replace('/', '_')}_{tf}.csv"
                df.to_csv(filename, index=False)
                print(f"Saved to {filename}")
            except Exception as e:
                print(f"Error fetching {symbol} {tf}: {e}")

if __name__ == "__main__":
    download_all_data()
