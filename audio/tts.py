import numpy as np
import torch
import sounddevice as sd


class TTS:
    def __init__(self, speaker: str = "aidar", sample_rate: int = 48000, device: str = "cpu"):
        self.sample_rate = sample_rate
        self.speaker = speaker
        self.device = torch.device(device)
        model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language="ru",
            speaker="v4_ru",
            trust_repo=True,
        )
        model.to(self.device)
        self.model = model

    def say(self, text: str) -> None:
        text = (text or "").strip()
        if not text:
            return
        print(f"[tts] {text}")
        try:
            audio = self.model.apply_tts(
                text=text, speaker=self.speaker, sample_rate=self.sample_rate
            )
            audio_np = audio.cpu().numpy().astype(np.float32)
            pad = np.zeros(int(self.sample_rate * 0.35), dtype=np.float32)
            audio_np = np.concatenate([audio_np, pad])
            sd.play(audio_np, self.sample_rate)
            sd.wait()
        except Exception as e:
            print(f"[tts error] {e}")
