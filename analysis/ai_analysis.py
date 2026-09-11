from datetime import datetime


def format_value(value, suffix=""):
    if value is None:
        return "veri yok"

    try:
        return f"{float(value):.2f}{suffix}"
    except Exception:
        return str(value)


def generate_fund_report(
    fund_code,
    fund_analysis=None,
    trend_analysis=None,
    flow_analysis=None,
    news=None
):
    """
    Fon verilerini tek bir okunabilir analiz raporuna dönüştürür.

    Bu fonksiyon doğrudan yatırım tavsiyesi vermez.
    Verileri yorumlamak için sinyal üretir.
    """

    fund_analysis = fund_analysis or {}
    trend_analysis = trend_analysis or {}
    flow_analysis = flow_analysis or {}
    news = news or []

    score = fund_analysis.get("score")
    signal = fund_analysis.get(
        "signal",
        "VERİ YOK"
    )

    monthly = fund_analysis.get(
        "monthly_return"
    )

    three_month = fund_analysis.get(
        "three_month_return"
    )

    momentum = fund_analysis.get(
        "momentum"
    )

    volatility = fund_analysis.get(
        "volatility"
    )

    drawdown = fund_analysis.get(
        "max_drawdown"
    )

    trend_data = trend_analysis.get(
        "trend",
        {}
    )

    trend = trend_data.get(
        "trend",
        "VERİ YOK"
    )

    trend_score = trend_data.get(
        "score"
    )

    change_data = trend_analysis.get(
        "change",
        {}
    )

    trend_changed = change_data.get(
        "changed",
        False
    )

    trend_direction = change_data.get(
        "direction",
        ""
    )

    flow_status = flow_analysis.get(
        "flow_status",
        "VERİ YOK"
    )

    flow_percent = flow_analysis.get(
        "flow_percent"
    )

    investor_change = flow_analysis.get(
        "investor_change"
    )

    report = []

    report.append(
        f"# {fund_code.upper()} Fon Analizi"
    )

    report.append("")

    report.append(
        f"Analiz zamanı: "
        f"{datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )

    report.append("")

    report.append("## Performans")

    report.append(
        f"- Aylık getiri: "
        f"{format_value(monthly, '%')}"
    )

    report.append(
        f"- 3 aylık getiri: "
        f"{format_value(three_month, '%')}"
    )

    report.append(
        f"- Momentum: "
        f"{format_value(momentum, '%')}"
    )

    report.append("")

    report.append("## Risk")

    report.append(
        f"- Volatilite: "
        f"{format_value(volatility, '%')}"
    )

    report.append(
        f"- Maksimum düşüş: "
        f"{format_value(drawdown, '%')}"
    )

    report.append("")

    report.append("## Trend")

    report.append(
        f"- Trend: {trend}"
    )

    report.append(
        f"- Trend skoru: "
        f"{format_value(trend_score)} / 100"
    )

    if trend_changed:
        report.append(
            f"- ⚠️ Trend değişimi: "
            f"{trend_direction}"
        )

    report.append("")

    report.append("## Para Akışı")

    report.append(
        f"- Durum: {flow_status}"
    )

    report.append(
        f"- Fon büyüklüğü değişimi: "
        f"{format_value(flow_percent, '%')}"
    )

    if investor_change is not None:

        direction = (
            "artış"
            if investor_change > 0
            else "azalış"
            if investor_change < 0
            else "değişim yok"
        )

        report.append(
            f"- Yatırımcı sayısı: "
            f"{investor_change:+d} ({direction})"
        )

    report.append("")

    report.append("## Genel Değerlendirme")

    if score is not None:

        if score >= 75:
            report.append(
                "🟢 Güçlü pozitif sinyal. "
                "Performans ve trend tarafı destekleyici."
            )

        elif score >= 60:
            report.append(
                "🟢 Pozitif görünüm. "
                "Trend destekliyor ancak risk göstergeleri "
                "ayrıca takip edilmeli."
            )

        elif score >= 45:
            report.append(
                "🟡 Nötr görünüm. "
                "Yeni trend oluşumu için daha fazla veri gerekli."
            )

        elif score >= 30:
            report.append(
                "🟠 Negatif görünüm. "
                "Momentum ve trend zayıflığı izlenmeli."
            )

        else:
            report.append(
                "🔴 Yüksek riskli görünüm. "
                "Trend ve performans belirgin şekilde zayıf."
            )

    if flow_percent is not None:

        if flow_percent > 1:

            report.append(
                "Fon büyüklüğünde artış görülüyor; "
                "para girişi sinyali mevcut."
            )

        elif flow_percent < -1:

            report.append(
                "Fon büyüklüğünde azalış görülüyor; "
                "para çıkışı sinyali mevcut."
            )

        else:

            report.append(
                "Fon büyüklüğünde belirgin bir akış "
                "sinyali görülmüyor."
            )

    report.append("")

    report.append("## Haberler")

    if news:

        for item in news[:5]:

            title = item.get(
                "title",
                ""
            )

            if title:
                report.append(
                    f"- {title}"
                )

    else:

        report.append(
            "Henüz haber verisi yok."
        )

    report.append("")

    report.append(
        "⚠️ Bu rapor otomatik veri analizi "
        "ve sinyal üretimidir; tek başına "
        "yatırım kararı için kullanılmamalıdır."
    )

    return "\n".join(report)


def generate_opportunity_signal(
    fund_analysis,
    trend_analysis,
    flow_analysis
):
    """
    Fırsat / takip / risk sınıflandırması.
    """

    score = fund_analysis.get("score")

    trend_data = trend_analysis.get(
        "trend",
        {}
    )

    trend_score = trend_data.get(
        "score"
    )

    flow_percent = flow_analysis.get(
        "flow_percent"
    )

    if score is None:
        return "VERİ YETERSİZ"

    positive = 0

    if score >= 60:
        positive += 1

    if (
        trend_score is not None
        and trend_score >= 60
    ):
        positive += 1

    if (
        flow_percent is not None
        and flow_percent > 1
    ):
        positive += 1

    if positive >= 3:
        return "GÜÇLÜ FIRSAT ADAYI"

    if positive == 2:
        return "POZİTİF TAKİP"

    if positive == 1:
        return "İZLE"

    return "RİSK / ZAYIF GÖRÜNÜM"
