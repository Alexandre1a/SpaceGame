import json
import os

SETTINGS_FILE = "settings.json"

# valeurs possibles
AVAILABLE_FPS = [
    24,
    30,
    60,
    120,
    144,
    240,
    380,
]  # 0 = illimité
AVAILABLE_RESOLUTIONS = [
    (800, 600),
    (1280, 720),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (3840, 2160),
]

DEFAULT_SETTINGS = {
    "fps": 120,
    "fullscreen": False,
    "resolution": (800, 600),
}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            # validation basique (si settings corrompus, fallback sur DEFAULT)
            if settings.get("fps") not in AVAILABLE_FPS:
                settings["fps"] = DEFAULT_SETTINGS["fps"]
            if tuple(settings.get("resolution", ())) not in AVAILABLE_RESOLUTIONS:
                settings["resolution"] = DEFAULT_SETTINGS["resolution"]
            return settings
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)
