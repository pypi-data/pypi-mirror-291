from abc import ABC, abstractmethod

from srai_telegrambot.dao_telegram_bot import DaoTelegramBot


class TelegramBotInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def message_admins(self, text: str):
        raise NotImplementedError()

    @abstractmethod
    def message_chat(self, chat_id: str, text: str):
        raise NotImplementedError()

    @abstractmethod
    def get_dao(self) -> DaoTelegramBot:
        raise NotImplementedError()
