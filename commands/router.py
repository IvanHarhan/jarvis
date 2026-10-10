import re

from commands.apps import try_launch
from commands.browser import (
    google,
    open_site,
    open_url,
    youtube_search,
)
from commands.system import (
    cancel_shutdown,
    lock_pc,
    mute,
    reboot_pc,
    set_volume,
    shutdown_pc,
    sleep_pc,
)
from commands.youtube import open_music, resume_series, search_and_play


NUM_WORDS = {
    "ноль": 0, "один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5,
    "шесть": 6, "семь": 7, "восемь": 8, "девять": 9, "десять": 10,
    "двадцать": 20, "тридцать": 30, "сорок": 40, "пятьдесят": 50,
    "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80, "девяносто": 90, "сто": 100,
}


def _extract_number(text: str) -> int | None:
    m = re.search(r"(\d{1,3})", text)
    if m:
        return int(m.group(1))
    total = 0
    found = False
    for word, val in NUM_WORDS.items():
        if re.search(rf"\b{word}\b", text):
            total += val
            found = True
    return total if found else None


VERB_LAUNCH = r"(?:запуст\w*|открой\w*|открыть|открыва\w*|включ\w*|врубай|врубить|поставь|погнали|продолж\w*)"
VERB_FIND = r"(?:найди|загугли|поищи|поиск)"
MUSIC_WORDS = r"(?:музыку|музыка|музло|музончик|музончика|плейлист|трек|треки)"


class Router:
    def __init__(self, tts):
        self.tts = tts
        self.rules = [
            # звук
            (r"\b(?:выключи|отключи|вырубай|вырубить)\s+(?:звук|громкость)|\bмьют\b", self._mute_on),
            (r"\b(?:включи|верни)\s+(?:звук|громкость)|\bразмьют\b", self._mute_off),
            (r"\b(?:громкость|звук)\b.*?(\d{1,3}|" + "|".join(NUM_WORDS) + ")", self._volume),
            # система
            (r"\b(?:заблокируй|блокируй|залочь|лочь|закрой\s+комп)\b", self._lock),
            (r"\b(?:спящий|сон|спать|усн[уи])\b", self._sleep),
            (r"\b(?:перезагруз)", self._reboot),
            (r"\b(?:выключи|выруби|отключи)\s+(?:комп|компьютер|пк)\b", self._shutdown),
            (r"\b(?:отмени|отменить)\s+(?:выключение|перезагруз)", self._cancel_shut),
            # поиск
            (rf"\b{VERB_FIND}\s+(.+)", self._google),
            # музыка
            (rf"\b{VERB_LAUNCH}\s+{MUSIC_WORDS}\b", self._music),
            (rf"^{MUSIC_WORDS}$", self._music),
            # ютуб с подсказкой типа "включи X на ютубе"
            (rf"\b{VERB_LAUNCH}\s+(.+?)\s+(?:на|в)\s+(?:ютубе|ютуб|youtube)\b", self._yt_what),
            (r"\b(?:ютуб|youtube)\s+(.+)", self._yt),
            # открой/включи/запусти ЧТО-ТО
            (rf"\b{VERB_LAUNCH}\s+(.+)", self._smart_launch),
        ]

    def route(self, text: str) -> None:
        text = (text or "").lower().strip().rstrip(".!?")
        if not text:
            return
        print(f"[router] '{text}'")
        for pattern, handler in self.rules:
            m = re.search(pattern, text)
            if m:
                try:
                    handler(m, text)
                except Exception as e:
                    print(f"[router error] {e}")
                    self.tts.say("ошибка")
                return
        self.tts.say("не понял")

    def _mute_on(self, m, t):
        mute(True)
        self.tts.say("звук выключен")

    def _mute_off(self, m, t):
        mute(False)
        self.tts.say("звук включен")

    def _volume(self, m, t):
        n = _extract_number(t)
        if n is None:
            self.tts.say("на сколько")
            return
        set_volume(n)
        self.tts.say(f"громкость {n}")

    def _lock(self, m, t):
        self.tts.say("блокирую")
        lock_pc()

    def _sleep(self, m, t):
        self.tts.say("ухожу в сон")
        sleep_pc()

    def _reboot(self, m, t):
        self.tts.say("перезагрузка через тридцать секунд, скажи отмени чтобы отменить")
        reboot_pc(30)

    def _shutdown(self, m, t):
        self.tts.say("выключаюсь через тридцать секунд, скажи отмени чтобы отменить")
        shutdown_pc(30)

    def _cancel_shut(self, m, t):
        cancel_shutdown()
        self.tts.say("отменено")

    def _google(self, m, t):
        q = m.group(1).strip()
        google(q)
        self.tts.say(f"гуглю {q}")

    def _yt(self, m, t):
        q = m.group(1).strip()
        search_and_play(q)
        self.tts.say(f"ютуб, {q}")

    def _yt_what(self, m, t):
        q = m.group(1).strip()
        search_and_play(q)
        self.tts.say(f"включаю {q}")

    def _music(self, m, t):
        open_music()
        self.tts.say("включаю музыку")

    def _smart_launch(self, m, t):
        name = m.group(1).strip()
        # 1) сайт по имени
        if open_site(name):
            self.tts.say(f"открываю {name}")
            return
        # 2) явный URL
        if name.startswith(("http://", "https://", "www.")) or (
            "." in name and " " not in name
        ):
            open_url(name if name.startswith("http") else f"https://{name}")
            self.tts.say("открываю")
            return
        # 3) приложение из конфига
        hit = try_launch(name)
        if hit:
            self.tts.say(f"запускаю {hit}")
            return
        # 4) ютуб: продолжить с того места где остановился
        resume_series(name)
        self.tts.say(f"продолжаю {name}")
