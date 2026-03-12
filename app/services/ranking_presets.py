PRESET_DEFINITIONS = {
    "balanced": {
        "label": "Balanced",
        "description": "General-purpose ranking across cost, safety, inclusivity, infrastructure, and community.",
        "weights": {
            "affordability": 1.2,
            "safety": 1.3,
            "inclusivity": 1.5,
            "internet": 1.0,
            "livability": 1.0,
            "community": 1.4,
        },
    },
    "best_for_remote_work": {
        "label": "Best for remote work",
        "description": "Prioritizes reliable internet, livability, and safety for long-term work stability.",
        "weights": {
            "affordability": 1.1,
            "safety": 1.4,
            "inclusivity": 1.1,
            "internet": 1.8,
            "livability": 1.5,
            "community": 1.1,
        },
    },
    "best_for_community": {
        "label": "Best for community",
        "description": "Prioritizes belonging, inclusivity, and queer community visibility.",
        "weights": {
            "affordability": 1.0,
            "safety": 1.2,
            "inclusivity": 1.8,
            "internet": 0.9,
            "livability": 1.0,
            "community": 2.0,
        },
    },
}


def get_preset(preset_key: str):
    return PRESET_DEFINITIONS.get(preset_key, PRESET_DEFINITIONS["balanced"])


def valid_preset(preset_key: str):
    return preset_key if preset_key in PRESET_DEFINITIONS else "balanced"
