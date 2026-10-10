"""Run ONE TIME to log into Google/YouTube in jarvis's browser profile.

После запуска:
  1. Откроется окно Chromium
  2. Залогинься в свой Google-аккаунт (тот, на котором ютуб с историей)
  3. Перейди на youtube.com — убедись что ты залогинен
  4. Закрой окно Chromium

Профиль сохранится в browser_profile/ и jarvis будет его использовать.
"""
from playwright.sync_api import sync_playwright
from config import BROWSER_PROFILE_DIR


def main():
    print(f"Профиль будет сохранён в: {BROWSER_PROFILE_DIR}")
    print("Залогинься в Google → перейди на youtube.com → закрой окно когда готов.\n")
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            BROWSER_PROFILE_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://accounts.google.com/")
        print("Жду пока закроешь браузер...")
        try:
            ctx.wait_for_event("close", timeout=600_000)
        except Exception:
            pass
        print("Готово. Профиль сохранён.")


if __name__ == "__main__":
    main()
