import pandas as pd
from .base_strategy import BaseStrategy

class FVGStrategy(BaseStrategy):
    def __init__(self, df):
        super().__init__(df)
        
    def add_indicators(self):
        # Trend Filter: 200 EMA
        self.df['ema200'] = self.df['close'].ewm(span=200, adjust=False).mean()
        
        # FVG Detection
        self.df['bullish_fvg'] = (self.df['low'].shift(-2) > self.df['high'])
        self.df['bullish_fvg_top'] = self.df['low'].shift(-2)
        self.df['bullish_fvg_bottom'] = self.df['high']
        
        self.df['bearish_fvg'] = (self.df['high'].shift(-2) < self.df['low'])
        self.df['bearish_fvg_top'] = self.df['low']
        self.df['bearish_fvg_bottom'] = self.df['high'].shift(-2)
        
        # Displacement Filter
        self.df['candle_body'] = abs(self.df['close'].shift(-1) - self.df['open'].shift(-1))
        self.df['body_sma20'] = self.df['candle_body'].rolling(window=20).mean()
        self.df['displacement'] = self.df['candle_body'] > (1.2 * self.df['body_sma20'])

    def run(self, initial_balance=10000, risk_per_trade=0.01):
        self.add_indicators()
        balance = initial_balance
        active_fvgs = []
        position = None
        self.equity_curve = [balance]
        
        for i in range(200, len(self.df) - 2):
            row = self.df.iloc[i]
            curr_price_low = row['low']
            curr_price_high = row['high']
            curr_price_close = row['close']
            curr_ema = row['ema200']
            
            # 1. Check for new FVGs
            if row['bullish_fvg'] and row['displacement']:
                active_fvgs.append({'type': 'bull', 'top': row['bullish_fvg_top'], 'bottom': row['bullish_fvg_bottom'], 'index': i})
            if row['bearish_fvg'] and row['displacement']:
                active_fvgs.append({'type': 'bear', 'top': row['bearish_fvg_top'], 'bottom': row['bearish_fvg_bottom'], 'index': i})
            
            # 2. Manage Position
            if position:
                if position['type'] == 'long':
                    if curr_price_low <= position['sl']:
                        exit_price = position['sl']
                        pnl = (exit_price - position['entry']) * position['size']
                        balance += pnl
                        self.trades.append({'type': 'long', 'entry': position['entry'], 'exit': exit_price, 'pnl': pnl, 'result': 'SL', 'time': row['datetime']})
                        position = None
                    elif not position['tp1_hit'] and curr_price_high >= position['tp1']:
                        pnl = (position['tp1'] - position['entry']) * (position['size'] * 0.5)
                        balance += pnl
                        position['tp1_hit'] = True
                        position['sl'] = position['entry'] 
                    elif position['tp1_hit'] and curr_price_high >= position['tp2']:
                        pnl = (position['tp2'] - position['entry']) * (position['size'] * 0.5)
                        balance += pnl
                        self.trades.append({'type': 'long', 'entry': position['entry'], 'exit': position['tp2'], 'pnl': pnl + (position['tp1'] - position['entry']) * (position['size'] * 0.5), 'result': 'TP2', 'time': row['datetime']})
                        position = None
                
                elif position['type'] == 'short':
                    if curr_price_high >= position['sl']:
                        exit_price = position['sl']
                        pnl = (position['entry'] - exit_price) * position['size']
                        balance += pnl
                        self.trades.append({'type': 'short', 'entry': position['entry'], 'exit': exit_price, 'pnl': pnl, 'result': 'SL', 'time': row['datetime']})
                        position = None
                    elif not position['tp1_hit'] and curr_price_low <= position['tp1']:
                        pnl = (position['entry'] - position['tp1']) * (position['size'] * 0.5)
                        balance += pnl
                        position['tp1_hit'] = True
                        position['sl'] = position['entry']
                    elif position['tp1_hit'] and curr_price_low <= position['tp2']:
                        pnl = (position['entry'] - position['tp2']) * (position['size'] * 0.5)
                        balance += pnl
                        self.trades.append({'type': 'short', 'entry': position['entry'], 'exit': position['tp2'], 'pnl': pnl + (position['entry'] - position['tp1']) * (position['size'] * 0.5), 'result': 'TP2', 'time': row['datetime']})
                        position = None
            
            # 3. Look for Entries
            if not position:
                for fvg in active_fvgs[:]:
                    if fvg['type'] == 'bull':
                        if curr_price_close > curr_ema:
                            if curr_price_low <= fvg['top'] and curr_price_close > fvg['bottom']:
                                if curr_price_close > row['open']:
                                    entry_price = curr_price_close
                                    sl = fvg['bottom']
                                    risk_amt = balance * risk_per_trade
                                    risk_per_share = entry_price - sl
                                    if risk_per_share > 0:
                                        size = risk_amt / risk_per_share
                                        tp1 = entry_price + (2 * risk_per_share)
                                        tp2 = entry_price + (4 * risk_per_share)
                                        position = {'type': 'long', 'entry': entry_price, 'sl': sl, 'tp1': tp1, 'tp2': tp2, 'size': size, 'tp1_hit': False}
                                        active_fvgs.remove(fvg)
                                        break
                    elif fvg['type'] == 'bear':
                        if curr_price_close < curr_ema:
                            if curr_price_high >= fvg['bottom'] and curr_price_close < fvg['top']:
                                if curr_price_close < row['open']:
                                    entry_price = curr_price_close
                                    sl = fvg['top']
                                    risk_amt = balance * risk_per_trade
                                    risk_per_share = sl - entry_price
                                    if risk_per_share > 0:
                                        size = risk_amt / risk_per_share
                                        tp1 = entry_price - (2 * risk_per_share)
                                        tp2 = entry_price - (4 * risk_per_share)
                                        position = {'type': 'short', 'entry': entry_price, 'sl': sl, 'tp1': tp1, 'tp2': tp2, 'size': size, 'tp1_hit': False}
                                        active_fvgs.remove(fvg)
                                        break
            
            if len(active_fvgs) > 20:
                active_fvgs.pop(0)
            self.equity_curve.append(balance)

        return self.trades, self.equity_curve
