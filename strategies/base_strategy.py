import pandas as pd

class BaseStrategy:
    def __init__(self, df):
        self.df = df.copy()
        self.trades = []
        self.equity_curve = []
        
    def add_indicators(self):
        """Override this method to add indicators to self.df."""
        pass
        
    def run(self, initial_balance=10000, risk_per_trade=0.01):
        """Override this method to implement the strategy logic."""
        raise NotImplementedError("Strategy must implement run() method.")
