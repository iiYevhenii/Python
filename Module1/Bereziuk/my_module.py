translations = {
    'uk': {
        'Language': 'Мова',
        'Ukrainian': 'Українська',
        'Speed': 'Швидкість',
        'km/h': 'км/год',
        'm/s': 'м/с',
        'less than': 'менша ніж',
        'greater than': 'більша ніж',
        'equal to': 'дорівнює'
    },
    'en': {
        'Language': 'Language',
        'Ukrainian': 'Ukrainian',
        'Speed': 'Speed',
        'km/h': 'km/h',
        'm/s': 'm/s',
        'less than': 'less than',
        'greater than': 'greater than',
        'equal to': 'equal to'
    }
}

def translate(text, lang='uk'):
    """Функція для перекладу тексту на основі словника."""
    if lang not in translations:
        lang = 'uk'
    return translations[lang].get(text, text)

def compare_speeds(v1_kmh, v2_ms):
    """
    Функція конвертує швидкості та порівнює їх.
    v1_kmh - швидкість в км/год
    v2_ms - швидкість в м/с
    Повертає словник з конвертованими даними та результатом порівняння.
    """
    v1_in_ms = v1_kmh / 3.6
    v2_in_kmh = v2_ms * 3.6

    if v1_kmh < v2_in_kmh:
        relation = 'less than'
    elif v1_kmh > v2_in_kmh:
        relation = 'greater than'
    else:
        relation = 'equal to'

    return {
        'v1_in_ms': v1_in_ms,
        'v2_in_kmh': v2_in_kmh,
        'relation': relation
    }