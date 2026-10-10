"""Show all audio input devices so you can pick one for config.INPUT_DEVICE."""
import sounddevice as sd


def main():
    print("=== INPUT DEVICES ===")
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0:
            mark = "  (default)" if i == sd.default.device[0] else ""
            print(f"  [{i}] {d['name']}{mark}")
    print()
    print("=== OUTPUT DEVICES ===")
    for i, d in enumerate(sd.query_devices()):
        if d["max_output_channels"] > 0:
            mark = "  (default)" if i == sd.default.device[1] else ""
            print(f"  [{i}] {d['name']}{mark}")
    print()
    print("Если хочешь использовать НЕ дефолтный микрофон —")
    print("в config.py поставь INPUT_DEVICE = <номер из списка выше>")


if __name__ == "__main__":
    main()
