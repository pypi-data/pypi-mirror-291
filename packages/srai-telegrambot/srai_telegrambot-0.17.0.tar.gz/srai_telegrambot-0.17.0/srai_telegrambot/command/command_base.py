from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext

from srai_telegrambot.telegram_bot_interface import TelegramBotInterface


class CommandBase(ABC):
    def __init__(self, command_name: str) -> None:
        self.command_name = command_name
        self.telegram_bot: TelegramBotInterface = None  # type: ignore

    def register(self, telegram_bot: TelegramBotInterface) -> None:
        if telegram_bot is None:
            raise ValueError("telegram_bot cannot be None")
        self.telegram_bot = telegram_bot

    def execute_command_callback(self, update: Update, context: CallbackContext) -> None:
        if self.telegram_bot is None:
            raise ValueError("Cannot run unregistered command")
        # update.message.to_dict()
        # message_id = str(update.message.message_id)
        # chat_id = str(update.message.chat_id)
        # author_id = str(update.message.from_user.id)
        # author_name = update.message.from_user.username
        # message_content = {"message_content_type": "text", "text": update.message.text}
        # message = ChatMessage(message_id, chat_id, author_id, author_name, message_content)
        # self.service_telegram_bot.dao_message.save_message(message)

        self.execute_command(str(update.message.chat_id), update.message.text)

    @abstractmethod
    def execute_command(self, chat_id: str, command_message: str) -> None:
        raise NotImplementedError()
