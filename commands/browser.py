import webbrowser
from urllib.parse import quote_plus


def open_url(url: str) -> None:
    webbrowser.open(url, new=2)


def youtube_search(query: str) -> None:
    open_url(f"https://www.youtube.com/results?search_query={quote_plus(query)}")


def youtube_first_result(query: str) -> None:
    open_url(f"https://www.youtube.com/results?search_query={quote_plus(query)}")


def google(query: str) -> None:
    open_url(f"https://www.google.com/search?q={quote_plus(query)}")


def open_site(name: str) -> bool:
    sites = {
        "ютуб": "https://youtube.com",
        "youtube": "https://youtube.com",
        "гугл": "https://google.com",
        "google": "https://google.com",
        "твич": "https://twitch.tv",
        "twitch": "https://twitch.tv",
        "бирж": "https://www.bybit.com/trade/usdt/BTCUSDT",
        "байбит": "https://www.bybit.com",
        "тв": "https://www.tradingview.com",
        "трейдингвью": "https://www.tradingview.com",
        "почт": "https://mail.google.com",
        "гитхаб": "https://github.com",
        "github": "https://github.com",
    }
    name = name.lower()
    for key, url in sites.items():
        if key in name:
            open_url(url)
            return True
    return False
