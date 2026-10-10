"""Pre-download Silero TTS + Whisper-small. Run once after install."""
import sys
import time


def warm_silero():
    print("[silero] loading...")
    t = time.time()
    import torch
    model, _ = torch.hub.load(
        repo_or_dir="snakers4/silero-models",
        model="silero_tts",
        language="ru",
        speaker="v4_ru",
        trust_repo=True,
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    audio = model.apply_tts(text="прогрев", speaker="aidar", sample_rate=48000)
    print(f"[silero] OK in {time.time()-t:.1f}s, audio len={len(audio)}")


def warm_whisper():
    print("[whisper] loading small on cuda/float16...")
    t = time.time()
    from faster_whisper import WhisperModel
    m = WhisperModel("small", device="cuda", compute_type="float16")
    print(f"[whisper] OK in {time.time()-t:.1f}s")


def warm_vosk():
    print("[vosk] loading model...")
    t = time.time()
    import vosk
    vosk.SetLogLevel(-1)
    m = vosk.Model("models/vosk-model-small-ru-0.22")
    print(f"[vosk] OK in {time.time()-t:.1f}s")


if __name__ == "__main__":
    try:
        warm_silero()
    except Exception as e:
        print(f"[silero FAIL] {e}", file=sys.stderr)
    try:
        warm_whisper()
    except Exception as e:
        print(f"[whisper FAIL] {e}", file=sys.stderr)
    try:
        warm_vosk()
    except Exception as e:
        print(f"[vosk FAIL] {e}", file=sys.stderr)
    print("=== warmup done ===")
