from pathlib import Path

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"

VOSK_MODEL_PATH = str(MODELS_DIR / "vosk-model-small-ru-0.22")

WAKE_WORDS = ["джарвис", "жарвис"]

WHISPER_MODEL_SIZE = "small"
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

TTS_SPEAKER = "aidar"
TTS_SAMPLE_RATE = 48000

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.008
SILENCE_DURATION = 2.0
MAX_COMMAND_SECONDS = 12

# Если хочешь конкретный микрофон — поставь номер из `python list_devices.py`.
# None = дефолтный микрофон винды.
INPUT_DEVICE = None

STEAM_GAMES = {}

APPS = {
    "хром": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "браузер": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "телеграм": r"C:\Users\harha\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "телега": r"C:\Users\harha\AppData\Roaming\Telegram Desktop\Telegram.exe",
}

BROWSER_PROFILE_DIR = str(BASE_DIR / "browser_profile")
MUSIC_URL = "https://music.youtube.com/"
