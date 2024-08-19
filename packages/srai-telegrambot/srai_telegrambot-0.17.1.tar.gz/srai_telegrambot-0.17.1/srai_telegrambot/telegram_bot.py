import logging
from typing import Dict
from uuid import uuid4

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Filters, MessageHandler, Updater

from srai_telegrambot.command.command_base import CommandBase
from srai_telegrambot.command.command_image_tag import get_image_tag
from srai_telegrambot.dao_telegram_bot import DaoTelegramBot
from srai_telegrambot.mode.text_mode_base import TextModeBase
from srai_telegrambot.mode.voice_mode_base import VoiceModeBase
from srai_telegrambot.model.chat_message import ChatMessage
from srai_telegrambot.telegram_bot_interface import TelegramBotInterface

logger = logging.getLogger(__name__)


class TelegramBot(TelegramBotInterface):
    def __init__(
        self,
        token: str,
        dao_telegram_bot: DaoTelegramBot,
    ):
        self.token = token
        self.dao_telegram_bot = dao_telegram_bot
        self.dispatcher: Dispatcher = None  # type: ignore
        self.list_admin_ids = []
        self.dict_text_mode: Dict[str, TextModeBase] = {}
        self.text_mode_default: TextModeBase = None  # type: ignore
        self.dict_voice_mode: Dict[str, VoiceModeBase] = {}
        self.voice_mode_default: VoiceModeBase = None  # type: ignore
        self.dict_command: Dict[str, CommandBase] = {}
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.updater = Updater(self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher  # type: ignore
        try:
            # on different commands - answer in Telegram

            # add text handler
            self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text))
            self.dispatcher.add_handler(MessageHandler(Filters.voice & ~Filters.command, self.handle_voice))

            # log all errors
            self.dispatcher.add_error_handler(self.error)  # type: ignore
        except Exception as e:
            self.message_admins(f"Error during startup with image tag {get_image_tag()}: {e}")
            raise e

    def get_dao(self) -> DaoTelegramBot:
        return self.dao_telegram_bot

    def register_admin(self, admin_id: str):
        self.list_admin_ids.append(admin_id)

    def register_text_mode(self, text_mode: TextModeBase, set_default: bool = False):
        if text_mode.text_mode_name in self.dict_text_mode:
            raise Exception(f"Mode name {text_mode.text_mode_name} already registered")
        self.dict_text_mode[text_mode.text_mode_name] = text_mode
        text_mode.register(self)
        if set_default:
            self.text_mode_default = text_mode

    def register_voice_mode(self, voice_mode: VoiceModeBase, set_default: bool = False):
        if voice_mode.voice_mode_name in self.dict_voice_mode:
            raise Exception(f"Mode name {voice_mode.voice_mode_name} already registered")
        self.dict_voice_mode[voice_mode.voice_mode_name] = voice_mode
        voice_mode.register(self)
        if set_default:
            self.voice_mode_default = voice_mode

    def register_command(self, command: CommandBase):
        if command.command_name in self.dict_command:
            raise Exception(f"Command name {command.command_name} already registered")
        self.dict_command[command.command_name] = command
        command.register(self)
        self.dispatcher.add_handler(CommandHandler(command.command_name, command.execute_command_callback))

    def handle_text(self, update: Update, context: CallbackContext):
        """Handle text messages."""
        message_id = str(update.message.message_id)
        chat_id = str(update.message.chat_id)
        author_id = str(update.message.from_user.id)
        author_name = update.message.from_user.username
        message_content = update.message.to_dict()
        message = ChatMessage(message_id, chat_id, author_id, author_name, message_content)
        self.dao_telegram_bot.save_message(message)
        # TODO also have this catch the bot messages
        if self.text_mode_default is not None:
            self.text_mode_default.handle_text(update, context)

    def handle_voice(self, update: Update, context: CallbackContext):
        """Handle text messages."""
        message_id = str(update.message.message_id)
        chat_id = str(update.message.chat_id)
        author_id = str(update.message.from_user.id)
        author_name = update.message.from_user.username
        message_content = update.message.to_dict()
        message = ChatMessage(message_id, chat_id, author_id, author_name, message_content)
        self.dao_telegram_bot.save_message(message)
        # TODO also have this catch the bot messages
        if self.voice_mode_default is not None:
            self.voice_mode_default.handle_voice(update, context)

    def message_admins(self, text: str):
        for admin_id in self.list_admin_ids:
            self.message_chat(chat_id=admin_id, text=text)

    def message_chat(self, chat_id: str, text: str):
        self.updater.bot.send_message(chat_id=chat_id, text=text)
        message_id = str(uuid4())
        message_content = {"message_content_type": "text", "text": text}
        self.dao_telegram_bot.save_message(ChatMessage(message_id, str(chat_id), "0", "bot", message_content))

    def error(self, update: Update, context: CallbackContext):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def main(self):
        """Start the bot."""

        self.message_admins(f"Startup succes with image tag {get_image_tag()}")

        #  Start the Bot
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()
