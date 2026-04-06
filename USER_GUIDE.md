# 🚀 Manus-Backtest-Pro User Guide

Welcome to your modular backtesting system! This project is designed to be simple for non-coders while being powerful enough to test any strategy you generate with ChatGPT.

## 🛠️ WSL Setup (One-time)

1.  **Open your WSL terminal.**
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/googial/Manus-Backtest-Pro.git
    cd Manus-Backtest-Pro
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your API keys:**
    - Copy `.env.example` to `.env`: `cp .env.example .env`
    - Open `.env` and add your Alpaca API Key and Secret.

## 📊 How to Run the Dashboard

1.  **Fetch Data (First time or to update):**
    ```bash
    python utils/data_fetcher.py
    ```
2.  **Start the Dashboard:**
    ```bash
    streamlit run dashboard/app.py
    ```
3.  **Open the URL** provided in the terminal (usually `http://localhost:8501`) in your browser.

## 🤖 How to Add ChatGPT Strategies

When you ask ChatGPT to create a strategy for this system, use this prompt:

> "Create a Python class for a backtesting strategy. It must inherit from `BaseStrategy` and implement the `run(self, initial_balance, risk_per_trade)` method. The class should add indicators to `self.df` in an `add_indicators()` method and then loop through the data to execute trades, appending them to `self.trades` and updating `self.equity_curve`."

### Steps to add it:
1.  **Save the code** ChatGPT gives you as a new file in the `strategies/` folder (e.g., `strategies/my_new_strategy.py`).
2.  **Register it** in `dashboard/app.py`:
    - Import it: `from strategies.my_new_strategy import MyNewStrategy`
    - Add it to the `strategies` dictionary: `strategies = {"FVG Strategy": FVGStrategy, "My New Strategy": MyNewStrategy}`

## 📈 Supported Assets
- **Crypto:** BTC/USD, ETH/USD, SOL/USD (via Alpaca)
- **Stocks:** NIFTY 50 (via Yahoo Finance)
- **Timeframes:** 1hr and 4hr
