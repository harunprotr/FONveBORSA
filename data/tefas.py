from curl_cffi import requests
import pandas as pd
from datetime import datetime, timedelta


TEFAS_URL = "https://www.tefas.gov.tr"


def get_session():
    return requests.Session(impersonate="chrome")


def get_fund_price_history(
    fund_code,
    start_date=None,
    end_date=None
):
    """
    TEFAS fon fiyat geçmişini çekmek için temel veri fonksiyonu.
    """

    if end_date is None:
        end_date = datetime.now()

    if start_date is None:
        start_date = end_date - timedelta(days=365)

    session = get_session()

    url = f"{TEFAS_URL}/api/DB/BindHistoryInfo"

    payload = {
        "fontip": "YAT",
        "fonkod": fund_code.upper(),
        "bastarih": start_date.strftime("%d.%m.%Y"),
        "bittarih": end_date.strftime("%d.%m.%Y"),
        "fonturk": "YAT"
    }

    response = session.post(
        url,
        data=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)


def get_latest_fund_data(fund_code):
    """
    Fonun son mevcut verisini almaya çalışır.
    """

    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)

    df = get_fund_price_history(
        fund_code,
        start_date,
        end_date
    )

    if df.empty:
        return None

    return df.iloc[-1].to_dict()


def calculate_returns(df):
    """
    Basit performans hesaplamaları.
    """

    if df.empty:
        return {}

    price_column = None

    for column in ["FIYAT", "FONUNV", "PRICE"]:
        if column in df.columns:
            price_column = column
            break

    if price_column is None:
        return {}

    prices = pd.to_numeric(
        df[price_column],
        errors="coerce"
    ).dropna()

    if len(prices) < 2:
        return {}

    result = {}

    result["daily"] = (
        (prices.iloc[-1] / prices.iloc[-2]) - 1
    ) * 100

    if len(prices) >= 22:
        result["monthly"] = (
            (prices.iloc[-1] / prices.iloc[-22]) - 1
        ) * 100

    if len(prices) >= 66:
        result["3_month"] = (
            (prices.iloc[-1] / prices.iloc[-66]) - 1
        ) * 100

    if len(prices) >= 132:
        result["6_month"] = (
            (prices.iloc[-1] / prices.iloc[-132]) - 1
        ) * 100

    if len(prices) >= 252:
        result["1_year"] = (
            (prices.iloc[-1] / prices.iloc[-252]) - 1
        ) * 100

    return result
