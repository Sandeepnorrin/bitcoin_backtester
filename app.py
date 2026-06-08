import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backtest import BacktestEngine, STRATEGIES
import os

st.set_page_config(page_title="BTC Strategy Backtester", layout="wide")

st.title("🚀 Bitcoin Strategy Backtester")
st.markdown("Backtest multiple strategies across different timeframes for the past 3 years.")

# Sidebar
st.sidebar.header("Configuration")
initial_capital = st.sidebar.number_input("Initial Capital ($)", value=10000.0, step=1000.0)
position_size_pct = st.sidebar.slider("Position Size per Trade (%)", 1, 100, 15) / 100.0

@st.cache_data
def load_data(timeframe):
    file_path = f"data/BTC_USDT_{timeframe}.csv"
    if not os.path.exists(file_path):
        return None
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

@st.cache_data
def run_backtest(strategy_name, timeframe, cap, pos_size):
    df = load_data(timeframe)
    if df is None:
        return None

    engine = BacktestEngine(initial_capital=cap, position_size_pct=pos_size)
    strategy_func = STRATEGIES[strategy_name]
    results = engine.run(df, strategy_func)
    return results

timeframes = ['5m', '15m', '1h', '4h', '1d']

if st.sidebar.button("Run All Backtests"):
    all_results = []

    progress_bar = st.progress(0)
    total_tasks = len(STRATEGIES) * len(timeframes)
    count = 0

    for strat_name in STRATEGIES.keys():
        for tf in timeframes:
            res = run_backtest(strat_name, tf, initial_capital, position_size_pct)
            if res:
                res_summary = {
                    'Strategy': strat_name,
                    'Timeframe': tf,
                    'Net Profit': res['Net Profit'],
                    'Total Trades': res['Total Trades'],
                    'Win Rate': res['Win Rate'],
                    'Max Drawdown': res['Max Drawdown'],
                    'Final Capital': res['Final Capital']
                }
                all_results.append(res_summary)

            count += 1
            progress_bar.progress(count / total_tasks)

    # Display Results
    st.header("📊 Top 2 Timeframes per Strategy")

    df_all = pd.DataFrame(all_results)

    for strat_name in STRATEGIES.keys():
        st.subheader(f"Strategy: {strat_name}")
        strat_df = df_all[df_all['Strategy'] == strat_name].sort_values(by='Net Profit', ascending=False)

        top_2 = strat_df.head(2)
        cols = st.columns(2)
        for i, (_, row) in enumerate(top_2.iterrows()):
            with cols[i]:
                color = "normal" if row['Net Profit'] >= 0 else "inverse"
                st.metric(f"Rank {i+1}: {row['Timeframe']}", f"${row['Net Profit']:,.2f}", delta=f"{row['Net Profit']/initial_capital*100:.1f}%")
                st.write(f"Win Rate: **{row['Win Rate']:.2f}%** | Trades: **{row['Total Trades']}**")
        st.divider()

    st.header("📈 Detailed Strategy Comparison")
    st.dataframe(df_all.sort_values(by='Net Profit', ascending=False), use_container_width=True)

    # Selection for detailed view
    st.header("🔍 Deep Dive")
    selected_strat = st.selectbox("Select Strategy for details", list(STRATEGIES.keys()))
    selected_tf = st.selectbox("Select Timeframe for details", timeframes)

    detail_res = run_backtest(selected_strat, selected_tf, initial_capital, position_size_pct)

    if detail_res and detail_res.get('trades'):
        st.write(f"Showing results for **{selected_strat}** on **{selected_tf}**")

        # Equity Curve
        trades_df = pd.DataFrame(detail_res['trades'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=trades_df['exit_time'], y=trades_df['capital'], mode='lines', name='Equity'))
        fig.update_layout(title=f"Equity Curve - {selected_strat} ({selected_tf})", xaxis_title="Date", yaxis_title="Capital ($)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Trade History")
        st.dataframe(trades_df, use_container_width=True)
    else:
        st.write("No trades executed for this combination.")

else:
    st.info("Click 'Run All Backtests' in the sidebar to start the analysis.")
    st.markdown("""
    ### Strategies Included:
    1. **10 EMA Jackpot**: Entries based on non-touching candles of the 10 EMA.
    2. **10 & 20 EMA Bumper**: EMA crossover confirmed by Marubozu candles.
    3. **5 EMA Reversal**: Reversal plays when price is outside the 5 EMA.
    4. **Triple Confirmation**: Alignment of 50 EMA, Supertrend, and VWAP.
    5. **50 EMA Reclaim**: Trading the reclaim of the 50 EMA after a retest.
    6. **Inside Candle**: Price action breakout from Mother/Child candle patterns.
    7. **12 PM Crypto**: Time-based breakout strategy (IST timezone).
    8. **Slow Stochastic**: Oscillator extremes with EMA trend filtering.
    """)
