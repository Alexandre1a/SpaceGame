import json
import os

SETTINGS_FILE = "settings.json"

AVAILABLE_FPS = [1, 30, 60, 120, 144, 240, 360]  # 0 = uncapped

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
    "resolution": (1280, 720),
}


def loadSettings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            if settings.get("fps") not in AVAILABLE_FPS:
                print(
                    f"[Settings] FPS invalide ({settings.get('fps')}), utilisation de la valeur par défaut"
                )
                settings["fps"] = DEFAULT_SETTINGS["fps"]

            if tuple(settings.get("resolution", ())) not in AVAILABLE_RESOLUTIONS:
                print(
                    f"[Settings] Résolution invalide ({settings.get('resolution')}), utilisation de la valeur par défaut"
                )
                settings["resolution"] = DEFAULT_SETTINGS["resolution"]

            print(f"[Settings] Paramètres chargés depuis {SETTINGS_FILE}")
            return settings
        except Exception as e:
            print(f"[Settings] Erreur lors du chargement : {e}")
            print(f"[Settings] Utilisation des paramètres par défaut")
            return DEFAULT_SETTINGS.copy()

    print(
        f"[Settings] Aucun fichier de paramètres trouvé, utilisation des valeurs par défaut"
    )
    return DEFAULT_SETTINGS.copy()


def saveSettings(settings):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        print(f"[Settings] Paramètres sauvegardés dans {SETTINGS_FILE}")
        return True
    except Exception as e:
        print(f"[Settings] Erreur lors de la sauvegarde : {e}")
        return False


def validateSettings(settings):
    validated = settings.copy()

    if validated.get("fps") not in AVAILABLE_FPS:
        validated["fps"] = DEFAULT_SETTINGS["fps"]

    if tuple(validated.get("resolution", ())) not in AVAILABLE_RESOLUTIONS:
        validated["resolution"] = DEFAULT_SETTINGS["resolution"]

    if not isinstance(validated.get("fullscreen"), bool):
        validated["fullscreen"] = DEFAULT_SETTINGS["fullscreen"]

    return validated


def resetSettings():
    settings = DEFAULT_SETTINGS.copy()
    saveSettings(settings)
    print("[Settings] Paramètres réinitialisés aux valeurs par défaut")
    return settings
