import yfinance as yf
import pandas as pd


def get_stock_history(
    symbol,
    period="1y",
    interval="1d"
):
    """
    Hisse fiyat geçmişini getirir.
    """

    symbol = symbol.upper().strip()

    if not symbol.endswith(".IS"):
        symbol = symbol + ".IS"

    data = yf.download(
        symbol,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False
    )

    if data.empty:
        return pd.DataFrame()

    return data


def get_stock_info(symbol):
    """
    Temel hisse bilgilerini getirir.
    """

    symbol = symbol.upper().strip()

    if not symbol.endswith(".IS"):
        symbol = symbol + ".IS"

    ticker = yf.Ticker(symbol)

    try:
        return ticker.info
    except Exception:
        return {}


def calculate_stock_indicators(data):
    """
    RSI, hareketli ortalamalar ve momentum
    gibi temel göstergeleri hesaplar.
    """

    if data.empty:
        return data

    if isinstance(data.columns, pd.MultiIndex):
        close = data["Close"].iloc[:, 0]
    else:
        close = data["Close"]

    close = pd.to_numeric(
        close,
        errors="coerce"
    )

    data["MA20"] = close.rolling(20).mean()
    data["MA50"] = close.rolling(50).mean()
    data["MA200"] = close.rolling(200).mean()

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, pd.NA)

    data["RSI"] = 100 - (
        100 / (1 + rs)
    )

    data["Momentum"] = (
        close / close.shift(20) - 1
    ) * 100

    return data


def analyze_stock(symbol):
    """
    Hisse için temel teknik analiz özeti.
    """

    data = get_stock_history(
        symbol,
        period="1y"
    )

    if data.empty:
        return {
            "symbol": symbol,
            "status": "VERI_YOK"
        }

    data = calculate_stock_indicators(data)

    if isinstance(data["Close"], pd.DataFrame):
        close = data["Close"].iloc[:, 0]
    else:
        close = data["Close"]

    last_price = float(close.iloc[-1])

    rsi = data["RSI"].iloc[-1]
    momentum = data["Momentum"].iloc[-1]

    signal = "NÖTR"

    if pd.notna(rsi) and rsi < 30:
        signal = "AŞIRI SATIM"

    elif pd.notna(rsi) and rsi > 70:
        signal = "AŞIRI ALIM"

    elif (
        pd.notna(momentum)
        and momentum > 0
        and last_price > data["MA50"].iloc[-1]
    ):
        signal = "POZİTİF TREND"

    elif (
        pd.notna(momentum)
        and momentum < 0
    ):
        signal = "NEGATİF TREND"

    return {
        "symbol": symbol.upper(),
        "price": last_price,
        "rsi": None if pd.isna(rsi) else float(rsi),
        "momentum": (
            None
            if pd.isna(momentum)
            else float(momentum)
        ),
        "signal": signal
    }
