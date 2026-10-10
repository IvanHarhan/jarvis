import json
import queue
import sounddevice as sd
import vosk


class WakeWordListener:
    def __init__(self, model_path: str, wake_words: list[str], samplerate: int = 16000, input_device=None):
        vosk.SetLogLevel(-1)
        self.model = vosk.Model(model_path)
        self.wake_words = [w.lower() for w in wake_words]
        self.samplerate = samplerate
        self.input_device = input_device
        self._q: queue.Queue = queue.Queue()

    def _callback(self, indata, frames, time, status):
        self._q.put(bytes(indata))

    def _match(self, text: str) -> str | None:
        text = text.lower()
        for w in self.wake_words:
            if w in text:
                return w
        return None

    def listen(self) -> str:
        rec = vosk.KaldiRecognizer(self.model, self.samplerate)
        with sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=4000,
            dtype="int16",
            channels=1,
            callback=self._callback,
            device=self.input_device,
        ):
            while True:
                data = self._q.get()
                if rec.AcceptWaveform(data):
                    text = json.loads(rec.Result()).get("text", "")
                    hit = self._match(text)
                    if hit:
                        return hit
                else:
                    partial = json.loads(rec.PartialResult()).get("partial", "")
                    hit = self._match(partial)
                    if hit:
                        rec.Reset()
                        while not self._q.empty():
                            self._q.get_nowait()
                        return hit
