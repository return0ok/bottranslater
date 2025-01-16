TOKEN = "7902705895:AAGfxPcuVbUSV1UAenw_qY-RJT4LPdLK98s"

LANGUAGES = {
    'ru': 'Russian 🇷🇺',
    'en': 'English 🇺🇸',
    'es': 'Spanish 🇪🇸',
    'uz': 'Uzbekistan 🇺🇿',
    'zh-cn': 'Chine 🇨🇳',
    'it': 'Italian 🇮🇹'

}


def get_key(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k