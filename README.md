# Jarvis — offline voice assistant (Russian)

**EN** · A local voice assistant for Windows: it listens for a wake word, understands a spoken command and answers with a synthesized voice. Everything runs on the PC — no cloud, no subscriptions.

**DE** · Ein lokaler Sprachassistent für Windows: Er wartet auf ein Aktivierungswort, erkennt den gesprochenen Befehl und antwortet mit synthetischer Stimme. Alles läuft auf dem eigenen PC – ohne Cloud und ohne Abo.

## How it works

```
microphone ──► Vosk (wake word, always on, cheap)
                 │  "jarvis…"
                 ▼
             faster-whisper (small, CUDA) ──► text of the command
                 │
                 ▼
             commands/  (Steam games, apps, YouTube/Google search, volume, lock, shutdown…)
                 │
                 ▼
             Silero TTS (voice "aidar") ──► spoken answer
```

- **Vosk** keeps listening for the wake word with very little CPU.
- **faster-whisper** only starts after the wake word, so the precise (heavier) recognition runs for a few seconds at a time.
- **Silero TTS** speaks the reply.
- Python 3.10+, tested on an RTX 3050 Ti laptop (falls back to CPU).

## Example commands

| said (Russian) | does |
|---|---|
| «запусти доту» | starts Dota 2 through Steam |
| «открой ютуб» | opens YouTube |
| «ютуб рик и морти» | searches YouTube |
| «загугли как сделать борщ» | Google search |
| «громкость 30» / «выключи звук» | system volume |
| «заблокируй» / «выключи комп» / «отмени выключение» | lock / shutdown / cancel |

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt
```

Download the Russian Vosk model `vosk-model-small-ru-0.22` from https://alphacephei.com/vosk/models and unpack it to `models\vosk-model-small-ru-0.22\`. Whisper and Silero download themselves on the first start.

```powershell
python main.py
```

When it says «я готов» it is listening.

## Configuration (`config.py`)

- `WAKE_WORDS` — activation phrases
- `STEAM_GAMES` — games by Steam AppID
- `APPS` — paths to your own programs
- `WHISPER_MODEL_SIZE` — `small` is enough for commands, `medium` is more accurate but slower
- no CUDA → `WHISPER_DEVICE = "cpu"`, `WHISPER_COMPUTE_TYPE = "int8"`
- the default Windows input can be a virtual device (e.g. Steam Streaming Microphone) — run `python list_devices.py` and set `INPUT_DEVICE`
