from srai_core.store.database_memory import DatabaseMemory

from srai_telegrambot.dao_telegram_bot import DaoTelegramBot
from srai_telegrambot.telegram_bot_interface import TelegramBotInterface


class TelegramBotTest(TelegramBotInterface):
    def __init__(self):
        self.dao_telegram_bot = DaoTelegramBot(DatabaseMemory())

    def message_admins(self, text: str):
        print(text)

    def message_chat(self, chat_id: str, text: str):
        print(text)

    def get_dao(self):
        return self.dao_telegram_bot
