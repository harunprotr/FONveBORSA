from data.news import search_market_news


def run():

    print("=" * 50)
    print("FONveBORSA OTOMATİK ANALİZ")
    print("=" * 50)

    print("\n[1] Piyasa haberleri taranıyor...")

    news = search_market_news()

    for item in news[:10]:

        title = item.get("title", "")

        if title:
            print("-", title)

    print("\n[2] Fon trend taraması hazırlanıyor...")
    print("[3] Para akışı taraması hazırlanıyor...")
    print("[4] BIST taraması hazırlanıyor...")
    print("[5] Fırsat/risk kontrolü hazırlanıyor...")

    print("\nANALİZ TAMAMLANDI.")


if __name__ == "__main__":
    run()
