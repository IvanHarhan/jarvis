import os
import subprocess
from config import STEAM_GAMES, APPS


def launch_steam_game(appid: int) -> None:
    os.startfile(f"steam://run/{appid}")


def try_launch(name: str) -> str | None:
    name = name.lower().strip()
    for key, appid in STEAM_GAMES.items():
        if key in name:
            launch_steam_game(appid)
            return key
    for key, path in APPS.items():
        if key in name:
            try:
                subprocess.Popen(path, shell=False)
            except FileNotFoundError:
                os.startfile(path)
            return key
    return None
