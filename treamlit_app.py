import streamlit as st
import pandas as pd
from analyzer import analyze_stock
from tickers import TICKERS

st.set_page_config(layout="wide")

st.title("🚀 AI Trading System Pro")

@st.cache_data(ttl=600)
def run_scan():
    results = []

    for t in TICKERS:
        try:
            res = analyze_stock(t)
            if res:
                results.append(res)
        except:
            continue

    return pd.DataFrame(results)

if st.button("开始扫描"):
    df = run_scan()

    if df.empty:
        st.warning("无有效数据")
    else:
        df = df.sort_values(by="Score", ascending=False)

        st.subheader("📊 全部结果")
        st.dataframe(df)

        st.subheader("🔥 TOP 5")
        st.dataframe(df.head(5))
