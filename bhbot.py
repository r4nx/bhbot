import os
import sys
from time import sleep
from functools import partial

import telebot
from requests.exceptions import RequestException
from pluginbase import PluginBase

from settings import SETTINGS
from bhbot.logger import get_logger
from bhbot.models import CommandDispatcher

here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

log = None


def error_handler(exctype, value, tb):
    log.error('An error has occurred.', exc_info=(exctype, value, tb))


def main():
    global log
    log = get_logger(__name__, file_name='bhbot.log')

    sys.excepthook = error_handler

    cmd_dispatcher = CommandDispatcher()

    # Load commands
    plugin_base = PluginBase(package='bhbot.plugins')
    command_source = plugin_base.make_plugin_source(
        searchpath=[get_path('default_commands')]
    )

    for command_name in command_source.list_plugins():
        log.info('Loading command {}..'.format(command_name))

        command = command_source.load_plugin(command_name)
        CommandClass = command.get_command()
        cmd = CommandClass()
        cmd.setup(cmd_dispatcher)

    tb = telebot.TeleBot(SETTINGS['BOT_TOKEN'])

    @tb.message_handler(func=lambda msg: msg.text is not None and \
        msg.text.startswith(SETTINGS['CMD_PREFIX']) and \
        msg.forward_date is None)
    def commands_handler(message):
        # Display help
        if message.text.startswith('!!'):
            commands = {}
            for trigger, cmd in sorted(cmd_dispatcher.commands.items()):
                commands.setdefault(cmd, []).append(trigger)

            triggers_list = [' '.join(triggers) for triggers in commands.values()]
            tb.send_message(message.chat.id, 'Commands list:\n' + '\n'.join(triggers_list))
            return

        # Dispatch command
        context = {'bot': tb, 'message': message}
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
