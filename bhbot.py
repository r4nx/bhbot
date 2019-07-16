from functools import partial
from time import sleep
import sys

import telebot
from requests.exceptions import RequestException

from logger import get_logger
from settings import SETTINGS
from models import CommandDispatcher
from default_commands.alive import AliveCommand


def error_handler(exctype, value, tb, log):
    log.error('An error has occurred.', exc_info=(exctype, value, tb))


def main():
    log = get_logger(__name__, file_name='bhbot.log')
    sys.excepthook = partial(error_handler, log=log)

    aliveCmd = AliveCommand(triggers=['alive'])
    
    cmd_dispatcher = CommandDispatcher()
    cmd_dispatcher.register_command(aliveCmd)

    tb = telebot.TeleBot(SETTINGS['BOT_TOKEN'])

    @tb.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith(SETTINGS['CMD_PREFIX']))
    def message_handler(message):
        context = {
            'bot': tb,
            'message': message
        }
        response = cmd_dispatcher.dispatch(message.text[len(SETTINGS['CMD_PREFIX']):], context)
        if response is not None:
            tb.send_message(message.chat.id, response)
    
    log.info('Bot started')
    print(tb.get_me())

    while True:
        try:
            tb.polling(none_stop=True)
            log.info('Bot stopped')
            break
        except RequestException:
            try:
                log.error('Connection lost, reconnecting in 5 seconds..')
                sleep(5)
            except (KeyboardInterrupt, EOFError, SystemExit):
                log.info('Exited manually during restart')
                break


if __name__ == '__main__':
    main()
