import os


SETTINGS = {
    'BOT_TOKEN': os.getenv('BHBOT_TOKEN', ''),
    'LOCALE': os.getenv('BHBOT_LOCALE', 'ru'),
    'CMD_PREFIX': os.getenv('BHBOT_CMD_PREFIX', '!')
}
