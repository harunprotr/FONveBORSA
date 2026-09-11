import pandas as pd
import numpy as np


def moving_average(prices, window):
    """Hareketli ortalama."""

    return prices.rolling(window).mean()


def calculate_trend(prices):
    """
    Kısa, orta ve uzun vadeli trendi belirler.
    """

    if prices is None or len(prices) < 50:
        return {
            "trend": "VERİ YETERSİZ",
            "score": None
        }

    prices = pd.to_numeric(
        prices,
        errors="coerce"
    ).dropna()

    if len(prices) < 50:
        return {
            "trend": "VERİ YETERSİZ",
            "score": None
        }

    ma20 = moving_average(prices, 20)
    ma50 = moving_average(prices, 50)

    current = prices.iloc[-1]
    current_ma20 = ma20.iloc[-1]
    current_ma50 = ma50.iloc[-1]

    score = 50

    # Fiyat / MA20
    if current > current_ma20:
        score += 15
    else:
        score -= 15

    # MA20 / MA50
    if current_ma20 > current_ma50:
        score += 20
    else:
        score -= 20

    # Son 10 günlük momentum
    if len(prices) >= 10:

        momentum = (
            current / prices.iloc[-10] - 1
        ) * 100

        if momentum > 3:
            score += 15

        elif momentum < -3:
            score -= 15

    score = max(
        0,
        min(100, score)
    )

    if score >= 75:
        trend = "GÜÇLÜ YÜKSELİŞ"

    elif score >= 60:
        trend = "YÜKSELİŞ"

    elif score >= 40:
        trend = "YATAY / İZLE"

    elif score >= 25:
        trend = "DÜŞÜŞ"

    else:
        trend = "GÜÇLÜ DÜŞÜŞ"

    return {
        "trend": trend,
        "score": score,
        "price": float(current),
        "ma20": float(current_ma20),
        "ma50": float(current_ma50)
    }


def detect_trend_change(prices):
    """
    Trendin yeni değişip değişmediğini kontrol eder.
    """

    if prices is None or len(prices) < 60:
        return {
            "changed": False,
            "direction": "UNKNOWN"
        }

    prices = pd.to_numeric(
        prices,
        errors="coerce"
    ).dropna()

    ma20 = prices.rolling(20).mean()
    ma50 = prices.rolling(50).mean()

    previous_difference = (
        ma20.iloc[-2] -
        ma50.iloc[-2]
    )

    current_difference = (
        ma20.iloc[-1] -
        ma50.iloc[-1]
    )

    if (
        previous_difference <= 0
        and current_difference > 0
    ):
        return {
            "changed": True,
            "direction": "POZİTİFE DÖNÜŞ"
        }

    if (
        previous_difference >= 0
        and current_difference < 0
    ):
        return {
            "changed": True,
            "direction": "NEGATİFE DÖNÜŞ"
        }

    return {
        "changed": False,
        "direction": "DEĞİŞİM YOK"
    }


def analyze_trend(prices):
    """
    Komple trend analizi.
    """

    trend = calculate_trend(prices)
    change = detect_trend_change(prices)

    return {
        "trend": trend,
        "change": change
    }
