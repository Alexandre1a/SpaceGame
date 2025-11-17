"""
Module de gestion des paramètres du jeu.
Gère le chargement, la sauvegarde et la validation des paramètres.
"""

import json
import os

SETTINGS_FILE = "settings.json"

# Valeurs disponibles pour les FPS
AVAILABLE_FPS = [1, 30, 60, 120, 144, 240, 360]  # 0 = illimité

# Résolutions disponibles
AVAILABLE_RESOLUTIONS = [
    (800, 600),
    (1280, 720),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (3840, 2160),
]

# Paramètres par défaut
DEFAULT_SETTINGS = {
    "fps": 120,
    "fullscreen": False,
    "resolution": (1280, 720),
}


def loadSettings():
    """
    Charge les paramètres depuis le fichier JSON.
    Si le fichier n'existe pas ou est corrompu, retourne les paramètres par défaut.

    Returns:
        Dictionnaire contenant les paramètres du jeu
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            # Validation des paramètres
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
    """
    Sauvegarde les paramètres dans le fichier JSON.

    Args:
        settings: Dictionnaire contenant les paramètres à sauvegarder

    Returns:
        True si la sauvegarde a réussi, False sinon
    """
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        print(f"[Settings] Paramètres sauvegardés dans {SETTINGS_FILE}")
        return True
    except Exception as e:
        print(f"[Settings] Erreur lors de la sauvegarde : {e}")
        return False


def validateSettings(settings):
    """
    Valide les paramètres et corrige les valeurs invalides.

    Args:
        settings: Dictionnaire des paramètres à valider

    Returns:
        Dictionnaire des paramètres validés et corrigés
    """
    validated = settings.copy()

    # Validation du FPS
    if validated.get("fps") not in AVAILABLE_FPS:
        validated["fps"] = DEFAULT_SETTINGS["fps"]

    # Validation de la résolution
    if tuple(validated.get("resolution", ())) not in AVAILABLE_RESOLUTIONS:
        validated["resolution"] = DEFAULT_SETTINGS["resolution"]

    # Validation du fullscreen (doit être un booléen)
    if not isinstance(validated.get("fullscreen"), bool):
        validated["fullscreen"] = DEFAULT_SETTINGS["fullscreen"]

    return validated


def resetSettings():
    """
    Réinitialise les paramètres aux valeurs par défaut.

    Returns:
        Dictionnaire des paramètres par défaut
    """
    settings = DEFAULT_SETTINGS.copy()
    saveSettings(settings)
    print("[Settings] Paramètres réinitialisés aux valeurs par défaut")
    return settings
