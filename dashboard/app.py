import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import sys

# Add parent directory to path to import strategies
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.fvg_strategy import FVGStrategy

st.set_page_config(page_title="Manus Backtest Pro", layout="wide")

st.title("📊 Manus Backtest Pro Dashboard")

# Sidebar for configuration
st.sidebar.header("Backtest Configuration")

# Asset Selection
data_files = [f for f in os.listdir("data") if f.endswith(".csv")]
selected_file = st.sidebar.selectbox("Select Asset Data", data_files)

# Strategy Selection
strategies = {"FVG Strategy": FVGStrategy}
selected_strategy_name = st.sidebar.selectbox("Select Strategy", list(strategies.keys()))

# Parameters
initial_balance = st.sidebar.number_input("Initial Balance ($)", value=10000)
risk_per_trade = st.sidebar.slider("Risk Per Trade (%)", 0.1, 5.0, 1.0) / 100

if st.sidebar.button("Run Backtest"):
    df = pd.read_csv(f"data/{selected_file}")
    
    strategy_class = strategies[selected_strategy_name]
    bt = strategy_class(df)
    
    with st.spinner("Running backtest..."):
        trades, equity_curve = bt.run(initial_balance=initial_balance, risk_per_trade=risk_per_trade)
    
    # Metrics
    final_balance = equity_curve[-1]
    total_return = (final_balance - initial_balance) / initial_balance * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Final Balance", f"${final_balance:,.2f}")
    col2.metric("Total Return", f"{total_return:.2f}%")
    col3.metric("Total Trades", len(trades))
    
    # Equity Curve Plot
    st.subheader("Equity Curve")
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=equity_curve, mode='lines', name='Equity'))
    fig.update_layout(xaxis_title="Bars", yaxis_title="Balance ($)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Trades Table
    if trades:
        st.subheader("Trade History")
        df_trades = pd.DataFrame(trades)
        st.dataframe(df_trades)
    else:
        st.info("No trades executed.")
else:
    st.info("Select parameters and click 'Run Backtest' to see results.")
