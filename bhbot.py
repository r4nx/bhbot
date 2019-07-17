from functools import partial
from time import sleep
import sys

import telebot
from requests.exceptions import RequestException

from logger import get_logger
from settings import SETTINGS
from models import CommandDispatcher
from default_commands.alive import AliveCommand
from default_commands.morning import MorningCommand
from default_commands.goodnight import GoodNightCommand
from default_commands.pseudowho import PseudoWhoCommand
from default_commands.pseudolist import PseudoListCommand
from default_commands.evgensim import EvgenSimulatorCommand
from default_commands.ask import AskCommand


log = None


def error_handler(exctype, value, tb):
    log.error('An error has occurred.', exc_info=(exctype, value, tb))


def main():
    global log
    log = get_logger(__name__, file_name='bhbot.log')

    sys.excepthook = error_handler

    alive_cmd = AliveCommand(triggers=['alive'])
    morning_cmd = MorningCommand(triggers=['morning', 'utro', 'ytro', 'утро'])
    goodnight_cmd = GoodNightCommand(triggers=['spok', 'спок'])
    pseudowho_cmd = PseudoWhoCommand(triggers=['who', 'кто', 'кому'])
    pseudolist_cmd = PseudoListCommand(triggers=['list', 'список'])
    evgensim_cmd = EvgenSimulatorCommand(triggers=['evgensim', 'evgen1137', 'евген'])
    ask_cmd = AskCommand(triggers=['ask', 'спрос'])

    cmd_dispatcher = CommandDispatcher()
    cmd_dispatcher.register_command(alive_cmd)
    cmd_dispatcher.register_command(morning_cmd)
    cmd_dispatcher.register_command(goodnight_cmd)
    cmd_dispatcher.register_command(pseudowho_cmd)
    cmd_dispatcher.register_command(pseudolist_cmd)
    cmd_dispatcher.register_command(evgensim_cmd)
    cmd_dispatcher.register_command(ask_cmd)

    tb = telebot.TeleBot(SETTINGS['BOT_TOKEN'])

    @tb.message_handler(func=lambda msg: msg.text is not None and msg.text.startswith(SETTINGS['CMD_PREFIX']))
    def message_handler(message):
        if message.text.startswith('!!'):
            commands = {}
            for trigger, cmd in sorted(cmd_dispatcher.commands.items()):
                commands.setdefault(cmd, []).append(trigger)
            tb.send_message(message.chat.id, 'Commands list:\n' + '\n'.join([' '.join(triggers) for triggers in commands.values()]))
            return
        context = {
            'bot': tb,
            'message': message
        }
        response = cmd_dispatcher.dispatch(message.text[len(SETTINGS['CMD_PREFIX']):], context)
        if response is not None:
            tb.send_message(message.chat.id, response)
    
    log.info('Bot started')

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
