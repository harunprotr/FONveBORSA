import streamlit as st
import pandas as pd

from data.tefas import (
    get_fund_price_history,
    calculate_returns
)

from data.bist import (
    analyze_stock
)

from data.news import (
    search_fund_news,
    search_stock_news
)

from analysis.fund_analysis import (
    analyze_fund
)

from analysis.trend_engine import (
    analyze_trend
)

from analysis.money_flow import (
    analyze_fund_flow
)

from analysis.ai_analysis import (
    generate_fund_report,
    generate_opportunity_signal
)


st.set_page_config(
    page_title="FONveBORSA",
    page_icon="📈",
    layout="wide"
)


st.title("📈 FONveBORSA")

st.caption(
    "TEFAS • BIST • Trend • Para Akışı • Haber • AI Analiz"
)


menu = st.sidebar.radio(
    "MENÜ",
    [
        "Ana Sayfa",
        "Fon Analizi",
        "Fon Karşılaştırma",
        "Trendler",
        "Para Akışı",
        "BIST",
        "Haberler",
        "Portföy",
        "Bildirimler"
    ]
)


# =========================================================
# ANA SAYFA
# =========================================================

if menu == "Ana Sayfa":

    st.header("📊 Piyasa Merkezi")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Fon Takibi",
        "Aktif"
    )

    col2.metric(
        "Trend Motoru",
        "Hazır"
    )

    col3.metric(
        "Para Akışı",
        "Hazır"
    )

    col4.metric(
        "BIST",
        "Hazır"
    )

    st.divider()

    st.subheader(
        "🚀 Sistem"
    )

    st.write(
        "FONveBORSA; fon, BIST, haber, "
        "trend ve para akışını tek ekranda "
        "birleştirmek için oluşturuluyor."
    )

    st.info(
        "Fon Analizi bölümünden bir TEFAS fon kodu "
        "girerek veri çekmeyi deneyebilirsin."
    )


# =========================================================
# FON ANALİZİ
# =========================================================

elif menu == "Fon Analizi":

    st.header("💰 Fon Analizi")

    fund_code = st.text_input(
        "Fon kodu",
        placeholder="Örn: KHA"
    )

    if st.button(
        "🔎 Analizi Başlat",
        use_container_width=True
    ):

        if not fund_code:

            st.warning(
                "Önce fon kodunu gir."
            )

        else:

            with st.spinner(
                f"{fund_code.upper()} verileri alınıyor..."
            ):

                try:

                    data = get_fund_price_history(
                        fund_code.upper()
                    )

                    if data.empty:

                        st.error(
                            "Fon verisi bulunamadı."
                        )

                    else:

                        st.success(
                            f"{fund_code.upper()} verisi alındı."
                        )

                        st.subheader(
                            "📊 Ham Veri"
                        )

                        st.dataframe(
                            data.tail(20),
                            use_container_width=True
                        )

                        # ---------------------------------
                        # Fiyat kolonu bul
                        # ---------------------------------

                        price_column = None

                        for column in [
                            "FIYAT",
                            "PRICE",
                            "FON_FIYAT",
                            "FonFiyat"
                        ]:

                            if column in data.columns:

                                price_column = column

                                break

                        if price_column is None:

                            st.warning(
                                "Fiyat sütunu otomatik bulunamadı."
                            )

                        else:

                            prices = pd.to_numeric(
                                data[price_column],
                                errors="coerce"
                            ).dropna()

                            # -----------------------------
                            # FON ANALİZİ
                            # -----------------------------

                            fund_analysis = analyze_fund(
                                data,
                                price_column
                            )

                            # -----------------------------
                            # TREND
                            # -----------------------------

                            trend_analysis = analyze_trend(
                                prices
                            )

                            # -----------------------------
                            # PARA AKIŞI
                            # -----------------------------

                            flow_analysis = {}

                            # -----------------------------
                            # HABER
                            # -----------------------------

                            news = search_fund_news(
                                fund_code.upper()
                            )

                            # -----------------------------
                            # AI RAPOR
                            # -----------------------------

                            report = generate_fund_report(
                                fund_code.upper(),
                                fund_analysis,
                                trend_analysis,
                                flow_analysis,
                                news
                            )

                            signal = generate_opportunity_signal(
                                fund_analysis,
                                trend_analysis,
                                flow_analysis
                            )

                            st.divider()

                            st.subheader(
                                "🎯 Sinyal"
                            )

                            st.metric(
                                "Fırsat / Risk",
                                signal
                            )

                            st.divider()

                            st.subheader(
                                "📈 Performans"
                            )

                            c1, c2, c3 = st.columns(3)

                            c1.metric(
                                "Günlük",
                                f"{fund_analysis.get('daily_return', 0):.2f}%"
                                if fund_analysis.get("daily_return") is not None
                                else "—"
                            )

                            c2.metric(
                                "Aylık",
                                f"{fund_analysis.get('monthly_return', 0):.2f}%"
                                if fund_analysis.get("monthly_return") is not None
                                else "—"
                            )

                            c3.metric(
                                "3 Ay",
                                f"{fund_analysis.get('three_month_return', 0):.2f}%"
                                if fund_analysis.get("three_month_return") is not None
                                else "—"
                            )

                            st.divider()

                            st.subheader(
                                "📈 Trend"
                            )

                            trend_data = trend_analysis.get(
                                "trend",
                                {}
                            )

                            c1, c2 = st.columns(2)

                            c1.metric(
                                "Trend",
                                trend_data.get(
                                    "trend",
                                    "—"
                                )
                            )

                            c2.metric(
                                "Trend Skoru",
                                trend_data.get(
                                    "score",
                                    "—"
                                )
                            )

                            st.divider()

                            st.subheader(
                                "🤖 Otomatik Analiz"
                            )

                            st.markdown(
                                report
                            )

                            st.divider()

                            st.subheader(
                                "📰 Son Haberler"
                            )

                            for item in news[:10]:

                                title = item.get(
                                    "title",
                                    ""
                                )

                                link = item.get(
                                    "link",
                                    ""
                                )

                                if title:

                                    st.markdown(
                                        f"- [{title}]({link})"
                                    )

                except Exception as error:

                    st.error(
                        "Veri alınırken hata oluştu."
                    )

                    st.code(
                        str(error)
                    )


# =========================================================
# BIST
# =========================================================

elif menu == "BIST":

    st.header("🏦 BIST Hisse Analizi")

    symbol = st.text_input(
        "Hisse kodu",
        placeholder="ASELS / FROTO / THYAO"
    )

    if st.button(
        "📊 Hisseyi Analiz Et",
        use_container_width=True
    ):

        if not symbol:

            st.warning(
                "Hisse kodunu gir."
            )

        else:

            with st.spinner(
                "Hisse analiz ediliyor..."
            ):

                try:

                    result = analyze_stock(
                        symbol
                    )

                    if result.get(
                        "status"
                    ) == "VERI_YOK":

                        st.error(
                            "Hisse verisi bulunamadı."
                        )

                    else:

                        c1, c2, c3 = st.columns(3)

                        c1.metric(
                            "Fiyat",
                            f"{result.get('price', 0):.2f}"
                        )

                        c2.metric(
                            "RSI",
                            f"{result.get('rsi', 0):.2f}"
                            if result.get("rsi") is not None
                            else "—"
                        )

                        c3.metric(
                            "Sinyal",
                            result.get(
                                "signal",
                                "—"
                            )
                        )

                        st.metric(
                            "Momentum",
                            f"{result.get('momentum', 0):.2f}%"
                            if result.get("momentum") is not None
                            else "—"
                        )

                        news = search_stock_news(
                            symbol.upper()
                        )

                        st.subheader(
                            "📰 Hisse Haberleri"
                        )

                        for item in news[:10]:

                            title = item.get(
                                "title",
                                ""
                            )

                            link = item.get(
                                "link",
                                ""
                            )

                            if title:

                                st.markdown(
                                    f"- [{title}]({link})"
                                )

                except Exception as error:

                    st.error(
                        "Hisse verisi alınamadı."
                    )

                    st.code(
                        str(error)
                    )


# =========================================================
# HABERLER
# =========================================================

elif menu == "Haberler":

    st.header(
        "📰 Piyasa Haberleri"
    )

    from data.news import (
        search_market_news
    )

    news = search_market_news()

    for item in news:

        title = item.get(
            "title",
            ""
        )

        link = item.get(
            "link",
            ""
        )

        source = item.get(
            "source",
            ""
        )

        if title:

            st.markdown(
                f"### [{title}]({link})"
            )

            if source:

                st.caption(
                    source
                )


# =========================================================
# DİĞER BÖLÜMLER
# =========================================================

elif menu == "Fon Karşılaştırma":

    st.header(
        "⚖️ Fon Karşılaştırma"
    )

    st.info(
        "Çoklu fon karşılaştırma motoru "
        "bir sonraki geliştirme aşamasında."
    )


elif menu == "Trendler":

    st.header(
        "📈 Trend Merkezi"
    )

    st.info(
        "Tüm fonları tarayan global trend tarayıcısı "
        "bir sonraki aşamada bağlanacak."
    )


elif menu == "Para Akışı":

    st.header(
        "💸 Para Akışı"
    )

    st.info(
        "Fon büyüklüğü + yatırımcı sayısı + "
        "rakip fon hareketleri birlikte analiz edilecek."
    )


elif menu == "Portföy":

    st.header(
        "💼 Portföyüm"
    )

    st.info(
        "Kendi fon ve hisselerini ekleyip "
        "toplam risk/getiri takibi yapabileceğin bölüm."
    )


elif menu == "Bildirimler":

    st.header(
        "🔔 Bildirim Merkezi"
    )

    st.write(
        "🌅 Sabah kontrolü — 10:30"
    )

    st.write(
        "☀️ Öğlen fırsat/risk taraması"
    )

    st.write(
        "🌙 Akşam piyasa özeti"
    )

    st.write(
        "🚨 Olağan dışı hareketlerde ek uyarı"
    )

    st.info(
        "Otomatik bildirim altyapısı "
        "GitHub Actions aşamasında bağlanacak."
    )


st.divider()

st.caption(
    "FONveBORSA • Fon + BIST + Trend + Para Akışı + AI"
)
