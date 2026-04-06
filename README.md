# 🚀 Manus-Backtest-Pro

## A Modular Backtesting System for Algorithmic Trading Strategies

Manus-Backtest-Pro is a user-friendly and modular backtesting system designed to help traders and enthusiasts test their algorithmic trading strategies. It supports multiple assets (cryptocurrencies and stocks) across various timeframes and features a Streamlit-based dashboard for interactive visualization and analysis of backtest results. The system is built to be easily extensible, allowing users to integrate new strategies, especially those generated with the help of AI tools like ChatGPT.

## ✨ Features

-   **Multi-Asset Data Fetching:** Supports BTC, ETH, SOL (via Alpaca) and NIFTY 50 (via Yahoo Finance).
-   **Multiple Timeframes:** Backtest strategies on 1-hour and 4-hour data.
-   **Modular Strategy Integration:** Easily add and test new strategies by extending a `BaseStrategy` class.
-   **Interactive Dashboard:** Visualize equity curves, trade history, and key performance metrics using a Streamlit web interface.
-   **WSL Compatibility:** Designed for seamless setup and operation on Windows Subsystem for Linux (WSL).

## 📁 Project Structure

```
Manus-Backtest-Pro/
├── .env.example              # Example environment variables for API keys
├── USER_GUIDE.md             # Detailed user guide (this file)
├── requirements.txt          # Python dependencies
├── dashboard/
│   └── app.py                # Streamlit dashboard application
├── data/                     # Directory to store downloaded historical data
├── strategies/
│   ├── base_strategy.py      # Base class for all trading strategies
│   └── fvg_strategy.py       # Example: Fair Value Gap (FVG) Strategy implementation
└── utils/
    └── data_fetcher.py       # Script for fetching historical market data
```

## 🛠️ Setup Instructions (WSL)

Follow these steps to get your backtesting environment up and running on your Windows Subsystem for Linux (WSL) instance.

1.  **Open your WSL terminal.**

2.  **Clone the repository:**

    ```bash
    git clone https://github.com/googial/Manus-Backtest-Pro.git
    cd Manus-Backtest-Pro
    ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API keys:**

    -   Copy the example environment file: `cp .env.example .env`
    -   Open the newly created `.env` file using a text editor (e.g., `nano .env` or `code .env` if you have VS Code integrated with WSL).
    -   Replace `your_api_key_here` and `your_secret_key_here` with your actual Alpaca API Key and Secret. Your `.env` file should look something like this:

        ```
        ALPACA_API_KEY="PK3QMSZCIAELDXZCQJ26NKUVO4"
        ALPACA_SECRET_KEY="8tj6nffbheFki2wUf8VpWVZ778AjapGKcFwTgaJ8V8R5"
        ```

## 📊 How to Run the Dashboard

1.  **Fetch Historical Data:**

    Before running any backtests, you need to download the historical data for the assets you want to test. This script will fetch data for BTC, ETH, SOL, and NIFTY 50.

    ```bash
    python utils/data_fetcher.py
    ```
    The data will be saved as CSV files in the `data/` directory.

2.  **Start the Streamlit Dashboard:**

    Navigate to the project root directory and run the Streamlit application:

    ```bash
    streamlit run dashboard/app.py
    ```

3.  **Access the Dashboard:**

    Streamlit will provide a local URL (usually `http://localhost:8501`) in your terminal. Open this URL in your web browser to access the interactive backtesting dashboard.

## 🤖 How to Add New Strategies (e.g., from ChatGPT)

The system is designed for easy integration of new trading strategies. You can even ask AI models like ChatGPT to generate strategy code for you!

### Prompting ChatGPT for a Strategy:

When asking ChatGPT to create a strategy, use a prompt similar to this:

> "Create a Python class for a backtesting strategy. It must inherit from `strategies.base_strategy.BaseStrategy` and implement the `run(self, initial_balance, risk_per_trade)` method. The class should add any necessary indicators to `self.df` within an `add_indicators()` method. The `run` method should contain the core trading logic, looping through the data to execute trades, appending them to `self.trades` (a list of dictionaries), and updating `self.equity_curve` (a list of balances) at each step."

### Steps to Integrate Your New Strategy:

1.  **Save the Strategy File:**

    Save the Python code provided by ChatGPT as a new `.py` file within the `strategies/` directory (e.g., `strategies/my_awesome_strategy.py`). Make sure the class name is unique (e.g., `MyAwesomeStrategy`).

2.  **Register the Strategy in the Dashboard:**

    You need to tell the dashboard about your new strategy. Open `dashboard/app.py` in a text editor and make the following two modifications:

    a.  **Import the Strategy Class:** Add an import statement at the top of the file:

        ```python
        from strategies.my_awesome_strategy import MyAwesomeStrategy
        ```

    b.  **Add to Strategy Dictionary:** Locate the `strategies` dictionary and add your new strategy to it:

        ```python
        strategies = {
            "FVG Strategy": FVGStrategy,
            "My Awesome Strategy": MyAwesomeStrategy, # Add this line
        }
        ```

3.  **Restart the Dashboard:**

    If your dashboard is already running, stop it (Ctrl+C in the terminal) and restart it using `streamlit run dashboard/app.py`. Your new strategy will now appear in the dropdown menu on the dashboard.

## 📈 Supported Assets and Timeframes

-   **Cryptocurrencies:** BTC/USD, ETH/USD, SOL/USD (Data sourced from Alpaca)
-   **Stocks:** NIFTY 50 (Data sourced from Yahoo Finance)
-   **Timeframes:** 1-Hour (1h) and 4-Hour (4h)

## 🤝 Contributing

Feel free to fork this repository, submit pull requests, or open issues if you have suggestions or encounter problems.

---

**Author:** Manus AI
**Date:** April 07, 2026
