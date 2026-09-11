import pandas as pd
import numpy as np


def calculate_return(prices, days):
    """Belirli gün aralığındaki getiriyi hesaplar."""

    if prices is None or len(prices) <= days:
        return None

    try:
        start = float(prices.iloc[-days - 1])
        end = float(prices.iloc[-1])

        if start == 0:
            return None

        return ((end / start) - 1) * 100

    except Exception:
        return None


def calculate_volatility(prices):
    """Günlük volatiliteyi hesaplar."""

    if prices is None or len(prices) < 20:
        return None

    returns = prices.pct_change().dropna()

    if returns.empty:
        return None

    return float(returns.std() * np.sqrt(252) * 100)


def calculate_drawdown(prices):
    """Maksimum düşüşü hesaplar."""

    if prices is None or prices.empty:
        return None

    prices = pd.to_numeric(
        prices,
        errors="coerce"
    ).dropna()

    if prices.empty:
        return None

    peak = prices.cummax()

    drawdown = (
        prices - peak
    ) / peak

    return float(drawdown.min() * 100)


def calculate_momentum(prices):
    """Fonun momentumunu hesaplar."""

    if prices is None or len(prices) < 20:
        return None

    current = float(prices.iloc[-1])
    previous = float(prices.iloc[-20])

    if previous == 0:
        return None

    return float(
        ((current / previous) - 1) * 100
    )


def score_fund(prices):
    """
    Fon için basit bir trend/risk skoru üretir.

    Bu skor yatırım tavsiyesi değildir.
    """

    if prices is None or len(prices) < 30:
        return {
            "score": None,
            "signal": "VERİ YETERSİZ"
        }

    daily = calculate_return(prices, 1)
    monthly = calculate_return(prices, 22)
    three_month = calculate_return(prices, 66)

    volatility = calculate_volatility(prices)
    drawdown = calculate_drawdown(prices)
    momentum = calculate_momentum(prices)

    score = 50

    if monthly is not None:

        if monthly > 10:
            score += 15

        elif monthly > 5:
            score += 8

        elif monthly < -10:
            score -= 15

        elif monthly < -5:
            score -= 8

    if three_month is not None:

        if three_month > 20:
            score += 15

        elif three_month > 10:
            score += 8

        elif three_month < -20:
            score -= 15

        elif three_month < -10:
            score -= 8

    if momentum is not None:

        if momentum > 5:
            score += 10

        elif momentum < -5:
            score -= 10

    if volatility is not None:

        if volatility > 40:
            score -= 5

        elif volatility < 15:
            score += 3

    if drawdown is not None and drawdown < -20:
        score -= 10

    score = max(
        0,
        min(100, score)
    )

    if score >= 75:
        signal = "GÜÇLÜ POZİTİF"

    elif score >= 60:
        signal = "POZİTİF"

    elif score >= 45:
        signal = "NÖTR / İZLE"

    elif score >= 30:
        signal = "NEGATİF"

    else:
        signal = "YÜKSEK RİSK"

    return {
        "score": score,
        "signal": signal,
        "daily_return": daily,
        "monthly_return": monthly,
        "three_month_return": three_month,
        "momentum": momentum,
        "volatility": volatility,
        "max_drawdown": drawdown
    }


def analyze_fund(data, price_column="FIYAT"):
    """
    TEFAS verisini analiz eder.
    """

    if data is None or data.empty:
        return {
            "status": "VERİ YOK"
        }

    if price_column not in data.columns:

        possible_columns = [
            "FIYAT",
            "PRICE",
            "FON_FIYAT",
            "FonFiyat"
        ]

        for column in possible_columns:

            if column in data.columns:
                price_column = column
                break

    if price_column not in data.columns:

        return {
            "status": "FİYAT SÜTUNU BULUNAMADI"
        }

    prices = pd.to_numeric(
        data[price_column],
        errors="coerce"
    ).dropna()

    result = score_fund(prices)

    result["status"] = "OK"

    return result
