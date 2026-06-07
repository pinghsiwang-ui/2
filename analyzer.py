import yfinance as yf
import pandas as pd
import ta
import time

def get_data(ticker, retries=3):
    for _ in range(retries):
        try:
            df = yf.download(ticker, period="1y", progress=False)
            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                return df
        except:
            time.sleep(1)
    return None


def analyze_stock(ticker):
    df = get_data(ticker)

    if df is None or df.empty:
        return None

    df = df.dropna()

    if len(df) < 60:
        return None

    close = df['Close'].astype(float)
    low_series = df['Low'].astype(float)
    high_series = df['High'].astype(float)

    ma50 = close.rolling(50).mean()
    ma200 = close.rolling(200).mean()

    rsi = ta.momentum.RSIIndicator(close).rsi()
    macd = ta.trend.MACD(close).macd()

    try:
        price = float(close.iloc[-1])
        ma50_last = float(ma50.iloc[-1])

        ma200_last = ma200.iloc[-1]
        if pd.isna(ma200_last):
            ma200_last = ma50_last
        else:
            ma200_last = float(ma200_last)

        rsi_last = float(rsi.iloc[-1])
        macd_last = float(macd.iloc[-1])

        low = float(low_series.tail(20).min())
        high = float(high_series.tail(20).max())

    except:
        return None

    score = 0

    # 趋势
    if price > ma200_last:
        score += 25
    if price > ma50_last:
        score += 15

    # 动量
    if 50 < rsi_last < 70:
        score += 15
    if macd_last > 0:
        score += 10

    # 支撑
    if (price - low) / price < 0.03:
        score += 25

    # 风险
    if price < ma50_last:
        score -= 10

    return {
        "Ticker": ticker,
        "Price": round(price, 2),
        "Score": score,
        "Support": round(low, 2),
        "Resistance": round(high, 2),
        "RSI": round(rsi_last, 1)
    }
