import os
import subprocess

try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    def _vol_iface():
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))

    def set_volume(percent: int) -> None:
        percent = max(0, min(100, percent))
        vol = _vol_iface()
        vol.SetMasterVolumeLevelScalar(percent / 100.0, None)

    def mute(state: bool = True) -> None:
        _vol_iface().SetMute(1 if state else 0, None)

except Exception:
    def set_volume(percent: int) -> None:
        pass

    def mute(state: bool = True) -> None:
        pass


def lock_pc() -> None:
    subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")


def sleep_pc() -> None:
    subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")


def shutdown_pc(seconds: int = 30) -> None:
    subprocess.Popen(f"shutdown /s /t {seconds}", shell=True)


def cancel_shutdown() -> None:
    subprocess.Popen("shutdown /a", shell=True)


def reboot_pc(seconds: int = 30) -> None:
    subprocess.Popen(f"shutdown /r /t {seconds}", shell=True)
