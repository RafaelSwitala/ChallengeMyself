UMLAUT_MAP = {
    "Ä": "Ae",
    "Ö": "Oe",
    "Ü": "Ue",
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
}

def replace_umlauts(text: str) -> str:
    if not isinstance(text, str):
        return text

    for umlaut, replacement in UMLAUT_MAP.items():
        text = text.replace(umlaut, replacement)

    return text
