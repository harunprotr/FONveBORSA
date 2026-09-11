import requests
import xml.etree.ElementTree as ET
from datetime import datetime


def get_google_news(query, limit=10):
    """
    Google News RSS üzerinden haberleri getirir.
    """

    url = "https://news.google.com/rss/search"

    params = {
        "q": query,
        "hl": "tr",
        "gl": "TR",
        "ceid": "TR:tr"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        root = ET.fromstring(
            response.content
        )

        news = []

        for item in root.findall(".//item")[:limit]:

            title = item.findtext(
                "title",
                ""
            )

            link = item.findtext(
                "link",
                ""
            )

            pub_date = item.findtext(
                "pubDate",
                ""
            )

            source = item.findtext(
                "source",
                ""
            )

            news.append({
                "title": title,
                "link": link,
                "published": pub_date,
                "source": source
            })

        return news

    except Exception as error:

        return [{
            "title": "Haber verisi alınamadı",
            "link": "",
            "published": "",
            "source": str(error)
        }]


def search_fund_news(fund_code):
    """
    Fonla ilgili haberleri arar.
    """

    return get_google_news(
        f"{fund_code} fon TEFAS"
    )


def search_stock_news(symbol):
    """
    Hisseyle ilgili haberleri arar.
    """

    return get_google_news(
        f"{symbol} hisse Borsa İstanbul"
    )


def search_market_news():
    """
    Genel piyasa haberlerini getirir.
    """

    return get_google_news(
        "Borsa İstanbul ekonomi finans piyasalar"
    )
