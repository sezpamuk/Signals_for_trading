import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="Credit & Equity Dashboard", layout="wide")
st.title("Credit & Equity PnL Dashboard")

# --- Credit Products (CDS Indexes) ---
st.header("Credit Products - CDS Indexes")
cds_indexes = ['CDX IG', 'CDX HY', 'iTraxx Europe', 'iTraxx Xover', 'CDX EM', 'CDX NA IG', 'CDX NA HY']
selected_cds = st.multiselect("Select CDS Indexes:", cds_indexes)

cds_dv01 = {}
for index in selected_cds:
    cds_dv01[index] = st.number_input(f"DV01 for {index}:", key=index, value=1.0)

# --- Equity Index Options ---
st.header("Equity Products - Stock Index Options")
equity_indexes = ['SPX', 'NDX']
selected_equities = st.multiselect("Select Equity Indexes:", equity_indexes)

equity_config = {}
for equity in selected_equities:
    st.markdown(f"**Configuration for {equity}:**")
    moneyness = st.selectbox(f"Moneyness for {equity}:", ['80%', '90%'], key=f"{equity}_moneyness")
    expiry = st.selectbox(f"Expiry for {equity}:", ['3M', '6M'], key=f"{equity}_expiry")
    equity_config[equity] = {"moneyness": moneyness, "expiry": expiry}

# --- Signal Configuration ---
st.header("Signal Configuration")
signal_type = st.radio("Signal Method", ["SMA", "EWMA"])
if signal_type == "SMA":
    sma_short = st.number_input("Short Horizon (days):", value=20)
    sma_long = st.number_input("Long Horizon (days):", value=100)
else:
    sma_long = st.number_input("SMA Long Horizon (days):", value=100)
    alpha = st.slider("EWMA Alpha (0–1):", min_value=0.0, max_value=1.0, value=0.1)

# --- Combine All Assets for Charting ---
all_assets = selected_cds + list(selected_equities)

# --- Signal Chart ---
st.header("Signal Chart")
signal_assets = st.multiselect("Select assets for signal chart:", all_assets)

if signal_assets:
    fig, ax = plt.subplots()
    x = np.linspace(0, 100, 100)
    for asset in signal_assets:
        if signal_type == "SMA":
            y = np.sin(x / 10 + np.random.rand()) + np.random.normal(0, 0.2, 100)
        else:
            y = np.exp(-alpha * x / 100) * np.sin(x / 10 + np.random.rand())
        ax.plot(x, y, label=f"{asset} ({signal_type})")
    ax.set_title("Signal Chart")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Please select one or more assets for the signal chart.")

# --- PnL Chart ---
st.header("PnL Chart")
pnl_assets = st.multiselect("Select assets for PnL chart:", all_assets)

if pnl_assets:
    fig, ax = plt.subplots()
    x = np.linspace(0, 100, 100)
    for asset in pnl_assets:
        y = np.cumsum(np.random.randn(100))  # Simulated PnL
        ax.plot(x, y, label=f"{asset}")
    ax.set_title("PnL Chart")
    ax.legend()
    st.pyplot(fig)
else:
    st.info("Please select one or more assets for the PnL chart.")

# --- Summary Table ---
st.subheader("Summary Table (Example)")
summary_df = pd.DataFrame({
    "Year": [2023, 2024],
    "Total PnL": [100000, 150000],
    "Options Cost": [5000, 7000]
})
st.dataframe(summary_df)
