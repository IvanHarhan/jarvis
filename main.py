import os
import sys
from pathlib import Path

os.environ["CT2_VERBOSE"] = "-1"

sys.path.insert(0, str(Path(__file__).parent))

from audio.stt import CommandListener
from audio.tts import TTS
from audio.wake import WakeWordListener
from commands.router import Router
from config import (
    INPUT_DEVICE,
    MAX_COMMAND_SECONDS,
    SAMPLE_RATE,
    SILENCE_DURATION,
    SILENCE_THRESHOLD,
    TTS_SAMPLE_RATE,
    TTS_SPEAKER,
    VOSK_MODEL_PATH,
    WAKE_WORDS,
    WHISPER_COMPUTE_TYPE,
    WHISPER_DEVICE,
    WHISPER_MODEL_SIZE,
)


def main():
    print("=== Jarvis запускается ===")
    print("[1/3] TTS (Silero) — может качать модель в первый раз...")
    tts = TTS(speaker=TTS_SPEAKER, sample_rate=TTS_SAMPLE_RATE)
    print("[2/3] STT (faster-whisper) — может качать модель в первый раз...")
    stt = CommandListener(
        model_size=WHISPER_MODEL_SIZE,
        device=WHISPER_DEVICE,
        compute_type=WHISPER_COMPUTE_TYPE,
        input_device=INPUT_DEVICE,
    )
    print("[3/3] Wake-word (Vosk)...")
    wake = WakeWordListener(VOSK_MODEL_PATH, WAKE_WORDS, samplerate=SAMPLE_RATE, input_device=INPUT_DEVICE)
    router = Router(tts)

    tts.say("я готов")
    print("\n>>> ВСЁ ГОТОВО. ГОВОРИ WAKE-WORD В МИКРОФОН <<<")
    print(">>> Прервать: Ctrl+C <<<\n")

    while True:
        print("[жду активацию]")
        word = wake.listen()
        print(f"[wake] поймал: '{word}'")
        tts.say("слушаю")
        text = stt.transcribe()
        print(f"[команда] '{text}'")
        if not text:
            tts.say("не услышал")
            continue
        router.route(text)


if __name__ == "__main__":
    import traceback
    try:
        main()
    except KeyboardInterrupt:
        print("\n[выход]")
    except Exception:
        print("\n===== CRASH =====")
        traceback.print_exc()
        input("\nНажми Enter чтобы закрыть...")
