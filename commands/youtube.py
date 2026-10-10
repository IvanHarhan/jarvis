"""YouTube helpers via playwright with persistent profile.

First-time setup: run `python setup_browser.py`, залогинься в Google/YouTube,
закрой окно. Дальше jarvis использует тот же профиль для:
  - открыть последнюю серию X из истории просмотров
  - открыть YouTube Music и продолжить слушать
"""
from __future__ import annotations

import threading
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

from config import BROWSER_PROFILE_DIR, MUSIC_URL


def _launch(headless: bool = False):
    """Return (playwright, context). Caller closes both."""
    p = sync_playwright().start()
    ctx = p.chromium.launch_persistent_context(
        BROWSER_PROFILE_DIR,
        headless=headless,
        viewport={"width": 1280, "height": 800},
        args=["--mute-audio"] if False else [],
    )
    return p, ctx


def _async(fn):
    """Run fn in a daemon thread so голосовой цикл не блокируется."""
    threading.Thread(target=fn, daemon=True).start()


def resume_series(query: str) -> None:
    """Find последнюю серию `query` в истории и кликнуть."""

    def worker():
        try:
            p, ctx = _launch()
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto("https://www.youtube.com/feed/history", wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
            # фильтр истории по запросу
            search = page.locator("input#search-input, input[aria-label*='Поиск']").first
            try:
                search.fill(query, timeout=4000)
                search.press("Enter")
                page.wait_for_timeout(2500)
            except Exception:
                # фолбэк — просто открой результаты поиска по сайту
                pass
            # первый видео-результат
            first = page.locator("ytd-video-renderer a#video-title, a#video-title-link").first
            try:
                first.click(timeout=4000)
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(3000)
            except Exception:
                pass
            # не закрываем контекст — оставляем браузер открытым с видео
        except Exception as e:
            print(f"[yt resume error] {e}")

    _async(worker)


def open_music() -> None:
    """Открыть YouTube Music и нажать play на первой карточке Quick picks."""

    def worker():
        try:
            p, ctx = _launch()
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto(MUSIC_URL, wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            # пробуем нажать play на первой карточке Quick Picks / Listen Again
            selectors = [
                "ytmusic-responsive-list-item-renderer .play-button",
                "ytmusic-card-shelf-renderer .play-button",
                "tp-yt-paper-icon-button[aria-label*='лосов']",
                "yt-icon-button#play-button",
            ]
            for sel in selectors:
                try:
                    page.locator(sel).first.click(timeout=2000)
                    return
                except Exception:
                    continue
            # фолбэк: клик по первой карточке
            try:
                page.locator("ytmusic-responsive-list-item-renderer").first.click(timeout=3000)
            except Exception:
                pass
        except Exception as e:
            print(f"[music error] {e}")

    _async(worker)


def search_and_play(query: str) -> None:
    """Открыть поиск YouTube по query и кликнуть на первый видео-результат."""

    def worker():
        try:
            p, ctx = _launch()
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto(
                f"https://www.youtube.com/results?search_query={quote_plus(query)}",
                wait_until="domcontentloaded",
            )
            page.wait_for_timeout(2000)
            try:
                page.locator("ytd-video-renderer a#video-title").first.click(timeout=3000)
            except Exception:
                pass
        except Exception as e:
            print(f"[yt search error] {e}")

    _async(worker)
