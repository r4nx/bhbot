from settings import SETTINGS

LOCALE_EN = {
    'CMD_NOT_FOUND': 'Command not found.',
    'EMPTY_CMD': 'No command name specified.'
}

LOCALE_RU = {
    'CMD_NOT_FOUND': 'Команда не найдена.',
    'EMPTY_CMD': 'Команда не указана.'
}

_LOCALES = {
    'en': LOCALE_EN,
    'ru': LOCALE_RU
}

def get_phrase(name: str, locale: str = SETTINGS['LOCALE']):
    # Trying to find specified locale, using english if no such was found,
    # then looking for phrase in that locale, if phrase was not found - making
    # last attempt and trying to get that phrase from english locale.
    return _LOCALES.get(locale, _LOCALES['en']) \
        .get(name, _LOCALES['en'].get(name, 'Cannot found phrase {}'.format(name)))
