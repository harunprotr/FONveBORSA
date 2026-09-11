import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="FONveBORSA",
    page_icon="📈",
    layout="wide"
)

st.title("📈 FONveBORSA")
st.caption("Fon • Borsa • Trend • Para Akışı • Yapay Zeka Analizi")

st.sidebar.header("Menü")

menu = st.sidebar.radio(
    "Bölüm seç",
    [
        "Ana Sayfa",
        "Fonlar",
        "Fon Karşılaştırma",
        "Trendler",
        "Para Akışı",
        "BIST",
        "Yapay Zeka",
        "Portföy",
        "Bildirimler"
    ]
)

st.sidebar.divider()
st.sidebar.info(
    f"Son güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
)

if menu == "Ana Sayfa":
    st.header("📊 Piyasa Genel Bakış")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Takip Edilen Fon", "0")
    col2.metric("Trend Sinyali", "—")
    col3.metric("Para Akışı", "—")
    col4.metric("BIST Durumu", "—")

    st.divider()

    st.subheader("🔥 Öne Çıkan Fırsatlar")

    st
