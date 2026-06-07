import pandas as pd
import pandas_ta as ta
import pytz

class BacktestEngine:
    def __init__(self, initial_capital=10000, position_size_pct=0.15):
        self.initial_capital = initial_capital
        self.position_size_pct = position_size_pct
        self.ist = pytz.timezone('Asia/Kolkata')

    def run(self, df, strategy_func):
        df = df.copy()
        if df['timestamp'].dtype != 'datetime64[ns]':
            try:
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            except:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True, drop=False)
        df = strategy_func(df)

        capital = self.initial_capital
        position = 0
        entry_price = 0
        trades = []

        trade_amount = self.initial_capital * self.position_size_pct

        for i in range(1, len(df)):
            # Check for entry
            if position == 0:
                if df.iloc[i].get('signal', 0) == 1: # Buy
                    entry_price = df.iloc[i]['close']
                    position = trade_amount / entry_price
                    entry_time = df.iloc[i]['timestamp']

                elif df.iloc[i].get('signal', 0) == -1: # Short
                    entry_price = df.iloc[i]['close']
                    position = - (trade_amount / entry_price)
                    entry_time = df.iloc[i]['timestamp']

            # Check for exit
            elif position > 0: # Long
                if df.iloc[i].get('exit_signal', 0) == 1:
                    exit_price = df.iloc[i]['close']
                    profit = position * (exit_price - entry_price)
                    capital += profit
                    trades.append({
                        'type': 'Long',
                        'entry_time': entry_time,
                        'exit_time': df.iloc[i]['timestamp'],
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'profit': profit,
                        'capital': capital
                    })
                    position = 0

            elif position < 0: # Short
                if df.iloc[i].get('exit_signal', 0) == -1:
                    exit_price = df.iloc[i]['close']
                    profit = abs(position) * (entry_price - exit_price)
                    capital += profit
                    trades.append({
                        'type': 'Short',
                        'entry_time': entry_time,
                        'exit_time': df.iloc[i]['timestamp'],
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'profit': profit,
                        'capital': capital
                    })
                    position = 0

        return self.calculate_metrics(trades, capital)

    def calculate_metrics(self, trades, final_capital):
        if not trades:
            return {
                'Net Profit': 0,
                'Total Trades': 0,
                'Win Rate': 0,
                'Max Drawdown': 0,
                'Final Capital': self.initial_capital,
                'trades': []
            }

        df_trades = pd.DataFrame(trades)
        win_rate = (df_trades['profit'] > 0).mean() * 100
        net_profit = final_capital - self.initial_capital

        df_trades['cum_capital'] = df_trades['capital']
        peak = df_trades['cum_capital'].expanding().max()
        drawdown = (peak - df_trades['cum_capital']) / peak
        max_dd = drawdown.max() * 100

        return {
            'Net Profit': net_profit,
            'Total Trades': len(trades),
            'Win Rate': win_rate,
            'Max Drawdown': max_dd,
            'Final Capital': final_capital,
            'trades': trades
        }

# Strategies
def strategy_10_ema_jackpot(df):
    df['ema10'] = ta.ema(df['close'], length=10)
    df['signal'] = 0
    df['exit_signal'] = 0

    for i in range(1, len(df)-1):
        if df.iloc[i]['close'] < df.iloc[i]['open'] and df.iloc[i]['low'] > df.iloc[i]['ema10']:
            if df.iloc[i+1]['high'] > df.iloc[i]['high']:
                df.at[df.index[i+1], 'signal'] = 1
        elif df.iloc[i]['close'] > df.iloc[i]['open'] and df.iloc[i]['high'] < df.iloc[i]['ema10']:
            if df.iloc[i+1]['low'] < df.iloc[i]['low']:
                df.at[df.index[i+1], 'signal'] = -1

    for i in range(1, len(df)):
        if df.iloc[i]['close'] < df.iloc[i]['ema10']:
            df.at[df.index[i], 'exit_signal'] = 1
        if df.iloc[i]['close'] > df.iloc[i]['ema10']:
            df.at[df.index[i], 'exit_signal'] = -1

    return df

def strategy_10_20_ema_bumper(df):
    df['ema10'] = ta.ema(df['close'], length=10)
    df['ema20'] = ta.ema(df['close'], length=20)
    df['signal'] = 0
    df['exit_signal'] = 0

    for i in range(1, len(df)):
        if df.iloc[i-1]['ema10'] <= df.iloc[i-1]['ema20'] and df.iloc[i]['ema10'] > df.iloc[i]['ema20']:
            body = abs(df.iloc[i]['close'] - df.iloc[i]['open'])
            candle_range = df.iloc[i]['high'] - df.iloc[i]['low']
            if candle_range > 0 and body / candle_range > 0.7 and df.iloc[i]['close'] > df.iloc[i]['open']:
                df.at[df.index[i], 'signal'] = 1
        elif df.iloc[i-1]['ema10'] >= df.iloc[i-1]['ema20'] and df.iloc[i]['ema10'] < df.iloc[i]['ema20']:
            body = abs(df.iloc[i]['close'] - df.iloc[i]['open'])
            candle_range = df.iloc[i]['high'] - df.iloc[i]['low']
            if candle_range > 0 and body / candle_range > 0.7 and df.iloc[i]['close'] < df.iloc[i]['open']:
                df.at[df.index[i], 'signal'] = -1

    for i in range(1, len(df)):
        if df.iloc[i]['ema10'] < df.iloc[i]['ema20']:
            df.at[df.index[i], 'exit_signal'] = 1
        if df.iloc[i]['ema10'] > df.iloc[i]['ema20']:
            df.at[df.index[i], 'exit_signal'] = -1
    return df

def strategy_5_ema_reversal(df):
    df['ema5'] = ta.ema(df['close'], length=5)
    df['ema20'] = ta.ema(df['close'], length=20)
    df['signal'] = 0
    df['exit_signal'] = 0
    for i in range(1, len(df)-1):
        if df.iloc[i]['high'] < df.iloc[i]['ema5']:
            if df.iloc[i+1]['high'] > df.iloc[i]['high']:
                df.at[df.index[i+1], 'signal'] = 1
        if df.iloc[i]['low'] > df.iloc[i]['ema5']:
            if df.iloc[i+1]['low'] < df.iloc[i]['low']:
                df.at[df.index[i+1], 'signal'] = -1
    for i in range(1, len(df)):
        if df.iloc[i]['close'] < df.iloc[i]['ema20']:
            df.at[df.index[i], 'exit_signal'] = 1
        if df.iloc[i]['close'] > df.iloc[i]['ema20']:
            df.at[df.index[i], 'exit_signal'] = -1
    return df

def strategy_triple_confirmation(df):
    df['ema50'] = ta.ema(df['close'], length=50)
    st = ta.supertrend(df['high'], df['low'], df['close'], length=20, multiplier=3)
    if st is not None:
        # Check for column names which can vary slightly by pandas-ta version
        col_name = 'SUPERTd_20_3.0' if 'SUPERTd_20_3.0' in st.columns else 'SUPERTd_20_3'
        df['st_dir'] = st[col_name]
    else:
        df['st_dir'] = 0
    df['vwap'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
    df['signal'] = 0
    df['exit_signal'] = 0
    for i in range(1, len(df)):
        if df.iloc[i]['st_dir'] == 1 and df.iloc[i-1]['st_dir'] == -1:
            if df.iloc[i]['close'] > df.iloc[i]['ema50']:
                if df['vwap'].iloc[i] and abs(df.iloc[i]['close'] - df.iloc[i]['vwap']) / df.iloc[i]['vwap'] < 0.01:
                    df.at[df.index[i], 'signal'] = 1
        elif df.iloc[i]['st_dir'] == -1 and df.iloc[i-1]['st_dir'] == 1:
            if df.iloc[i]['close'] < df.iloc[i]['ema50']:
                if df['vwap'].iloc[i] and abs(df.iloc[i]['close'] - df.iloc[i]['vwap']) / df.iloc[i]['vwap'] < 0.01:
                    df.at[df.index[i], 'signal'] = -1
    for i in range(1, len(df)):
        if df.iloc[i]['st_dir'] == -1:
            df.at[df.index[i], 'exit_signal'] = 1
        if df.iloc[i]['st_dir'] == 1:
            df.at[df.index[i], 'exit_signal'] = -1
    return df

def strategy_50_ema_reclaim(df):
    df['ema50'] = ta.ema(df['close'], length=50)
    df['signal'] = 0
    df['exit_signal'] = 0
    for i in range(5, len(df)-2):
        if df.iloc[i-1]['close'] < df.iloc[i-1]['ema50'] and df.iloc[i]['close'] > df.iloc[i]['ema50']:
            if i+2 < len(df):
                c1 = df.iloc[i+1]
                c2 = df.iloc[i+2]
                if c1['close'] < c1['open'] and c1['low'] > c1['ema50'] and \
                   c2['close'] < c2['open'] and c2['low'] > c2['ema50']:
                    high_to_break = max(c1['high'], c2['high'])
                    for j in range(i+3, min(i+10, len(df))):
                        if df.iloc[j]['high'] > high_to_break:
                            df.at[df.index[j], 'signal'] = 1
                            break
        elif df.iloc[i-1]['close'] > df.iloc[i-1]['ema50'] and df.iloc[i]['close'] < df.iloc[i]['ema50']:
            if i+2 < len(df):
                c1 = df.iloc[i+1]
                c2 = df.iloc[i+2]
                if c1['close'] > c1['open'] and c1['high'] < c1['ema50'] and \
                   c2['close'] > c2['open'] and c2['high'] < c2['ema50']:
                    low_to_break = min(c1['low'], c2['low'])
                    for j in range(i+3, min(i+10, len(df))):
                        if df.iloc[j]['low'] < low_to_break:
                            df.at[df.index[j], 'signal'] = -1
                            break
    for i in range(1, len(df)):
        if df.iloc[i]['close'] < df.iloc[i]['ema50']:
            df.at[df.index[i], 'exit_signal'] = 1
        if df.iloc[i]['close'] > df.iloc[i]['ema50']:
            df.at[df.index[i], 'exit_signal'] = -1
    return df

def strategy_inside_candle(df):
    df['signal'] = 0
    df['exit_signal'] = 0
    for i in range(1, len(df)-5):
        mother = df.iloc[i]
        child = df.iloc[i+1]
        # More robust inside candle definition
        if child['high'] <= mother['high'] and child['low'] >= mother['low']:
            # Breakout of mother candle
            for j in range(i+2, min(i+10, len(df))):
                if df.iloc[j]['high'] > mother['high']:
                    df.at[df.index[j], 'signal'] = 1
                    # Simple exit after 5 candles or opposite extreme
                    exit_idx = min(j+5, len(df)-1)
                    df.at[df.index[exit_idx], 'exit_signal'] = 1
                    break
                elif df.iloc[j]['low'] < mother['low']:
                    df.at[df.index[j], 'signal'] = -1
                    exit_idx = min(j+5, len(df)-1)
                    df.at[df.index[exit_idx], 'exit_signal'] = -1
                    break
    return df

def strategy_12_pm_crypto(df):
    df['signal'] = 0
    df['exit_signal'] = 0
    ist = pytz.timezone('Asia/Kolkata')
    df['timestamp_ist'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert(ist)
    for i in range(len(df)-5):
        dt = df.iloc[i]['timestamp_ist']
        if dt.hour == 12 and dt.minute == 0:
            h = df.iloc[i]['high']
            l = df.iloc[i]['low']
            for j in range(i+1, i+4):
                if df.iloc[j]['high'] > h:
                    df.at[df.index[j], 'signal'] = 1
                    for k in range(j+1, min(j+48, len(df))):
                        if df.iloc[k]['timestamp_ist'].hour == 14:
                            df.at[df.index[k], 'exit_signal'] = 1
                            break
                    break
                elif df.iloc[j]['low'] < l:
                    df.at[df.index[j], 'signal'] = -1
                    for k in range(j+1, min(j+48, len(df))):
                        if df.iloc[k]['timestamp_ist'].hour == 14:
                            df.at[df.index[k], 'exit_signal'] = -1
                            break
                    break
    return df

def strategy_slow_stochastic(df):
    stoch = ta.stoch(df['high'], df['low'], df['close'], k=9, d=3, smooth_k=3)
    if stoch is not None:
        df['stoch_k'] = stoch['STOCHk_9_3_3']
    else:
        df['stoch_k'] = 50
    df['ema20'] = ta.ema(df['close'], length=20)
    df['signal'] = 0
    df['exit_signal'] = 0
    for i in range(1, len(df)):
        if df.iloc[i-1]['stoch_k'] < 10 and df.iloc[i]['stoch_k'] > 10:
            if df.iloc[i]['close'] > df.iloc[i]['ema20']:
                df.at[df.index[i], 'signal'] = 1
        elif df.iloc[i-1]['stoch_k'] > 90 and df.iloc[i]['stoch_k'] < 90:
            if df.iloc[i]['close'] < df.iloc[i]['ema20']:
                df.at[df.index[i], 'signal'] = -1
    for i in range(1, len(df)):
        if df.iloc[i]['stoch_k'] > 80:
            df.at[df.index[i], 'exit_signal'] = 1
        if df.iloc[i]['stoch_k'] < 20:
            df.at[df.index[i], 'exit_signal'] = -1
    return df

STRATEGIES = {
    "10 EMA Jackpot": strategy_10_ema_jackpot,
    "10 & 20 EMA Bumper": strategy_10_20_ema_bumper,
    "5 EMA Reversal": strategy_5_ema_reversal,
    "Triple Confirmation": strategy_triple_confirmation,
    "50 EMA Reclaim": strategy_50_ema_reclaim,
    "Inside Candle": strategy_inside_candle,
    "12 PM Crypto": strategy_12_pm_crypto,
    "Slow Stochastic": strategy_slow_stochastic
}
