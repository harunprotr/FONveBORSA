import pandas as pd
import numpy as np


def calculate_asset_flow(
    current_value,
    previous_value
):
    """
    Fon büyüklüğündeki değişimden
    yaklaşık net para hareketini hesaplar.
    """

    if current_value is None or previous_value is None:
        return None

    try:
        current = float(current_value)
        previous = float(previous_value)

        return current - previous

    except Exception:
        return None


def calculate_flow_percent(
    current_value,
    previous_value
):
    """
    Fon büyüklüğündeki yüzdesel değişim.
    """

    if current_value is None or previous_value in [None, 0]:
        return None

    try:
        return (
            (float(current_value) /
             float(previous_value)) - 1
        ) * 100

    except Exception:
        return None


def classify_flow(flow_percent):
    """
    Para hareketinin yönünü sınıflandırır.
    """

    if flow_percent is None:
        return "VERİ YOK"

    if flow_percent >= 5:
        return "GÜÇLÜ PARA GİRİŞİ"

    if flow_percent >= 1:
        return "PARA GİRİŞİ"

    if flow_percent <= -5:
        return "GÜÇLÜ PARA ÇIKIŞI"

    if flow_percent <= -1:
        return "PARA ÇIKIŞI"

    return "NÖTR"


def analyze_fund_flow(
    current_size,
    previous_size,
    current_investors=None,
    previous_investors=None
):
    """
    Fon büyüklüğü ve yatırımcı sayısını birlikte analiz eder.
    """

    flow = calculate_asset_flow(
        current_size,
        previous_size
    )

    flow_percent = calculate_flow_percent(
        current_size,
        previous_size
    )

    investor_change = None

    if (
        current_investors is not None
        and previous_investors is not None
    ):
        try:
            investor_change = (
                int(current_investors)
                - int(previous_investors)
            )
        except Exception:
            investor_change = None

    return {
        "estimated_flow": flow,
        "flow_percent": flow_percent,
        "flow_status": classify_flow(flow_percent),
        "investor_change": investor_change
    }


def compare_funds_flow(funds):
    """
    Birden fazla fonu para akışına göre sıralar.

    funds örneği:

    [
        {
            "code": "KHA",
            "current_size": 100,
            "previous_size": 90
        }
    ]
    """

    results = []

    for fund in funds:

        current = fund.get(
            "current_size"
        )

        previous = fund.get(
            "previous_size"
        )

        flow = calculate_asset_flow(
            current,
            previous
        )

        flow_percent = calculate_flow_percent(
            current,
            previous
        )

        results.append({
            "code": fund.get("code"),
            "flow": flow,
            "flow_percent": flow_percent
        })

    results.sort(
        key=lambda x: (
            x["flow_percent"]
            if x["flow_percent"] is not None
            else -999999
        ),
        reverse=True
    )

    return results


def detect_possible_money_destination(
    losing_fund,
    competing_funds
):
    """
    Bir fondan çıkış görülürken rakip fonlarda
    aynı dönemde güçlü giriş varsa olası para
    yönünü tespit eder.

    Kesin yatırımcı transferi değildir;
    korelasyon/olasılık sinyalidir.
    """

    losing_flow = losing_fund.get(
        "flow_percent"
    )

    if losing_flow is None or losing_flow >= 0:
        return []

    destinations = []

    for fund in competing_funds:

        flow = fund.get(
            "flow_percent"
        )

        if flow is None:
            continue

        if flow > 1:

            destinations.append({
                "code": fund.get("code"),
                "flow_percent": flow,
                "possible_destination": True
            })

    destinations.sort(
        key=lambda x: x["flow_percent"],
        reverse=True
    )

    return destinations
