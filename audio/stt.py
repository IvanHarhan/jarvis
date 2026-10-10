import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


class CommandListener:
    def __init__(
        self,
        model_size: str = "small",
        device: str = "cuda",
        compute_type: str = "float16",
        input_device=None,
    ):
        self.input_device = input_device
        try:
            self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        except Exception:
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def _record(
        self,
        samplerate: int = 16000,
        max_seconds: float = 10.0,
        silence_threshold: float = 0.012,
        silence_duration: float = 1.2,
    ) -> np.ndarray:
        block_duration = 0.1
        blocksize = int(samplerate * block_duration)
        buffer: list[np.ndarray] = []
        silent = 0
        spoke = False
        max_silent = int(silence_duration / block_duration)
        max_blocks = int(max_seconds / block_duration)

        with sd.InputStream(
            samplerate=samplerate, channels=1, dtype="float32", blocksize=blocksize,
            device=self.input_device,
        ) as stream:
            for _ in range(max_blocks):
                block, _ = stream.read(blocksize)
                buffer.append(block.copy())
                rms = float(np.sqrt(np.mean(block ** 2)))
                if rms < silence_threshold:
                    silent += 1
                    if spoke and silent >= max_silent:
                        break
                else:
                    spoke = True
                    silent = 0

        return np.concatenate(buffer).flatten()

    def transcribe(self) -> str:
        audio = self._record()
        if len(audio) == 0:
            return ""
        segments, _ = self.model.transcribe(
            audio,
            language="ru",
            beam_size=5,
            vad_filter=True,
            initial_prompt=(
                "Команды голосовому ассистенту на русском языке. "
                "Запусти, включи, открой, найди, загугли, ютуб, гугл. "
                "Дота, кс, зомбоид, кербал, раст. "
                "Хром, телеграм, блокнот, тв, байбит, гитхаб. "
                "Рик и Морти, Кухня, Игра Престолов. "
                "Громкость, звук, заблокируй, перезагрузка, выключи."
            ),
        )
        return " ".join(s.text.strip() for s in segments).strip()
