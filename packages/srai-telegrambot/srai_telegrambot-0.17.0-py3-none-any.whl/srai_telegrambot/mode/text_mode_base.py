import hashlib
from abc import ABC, abstractmethod
from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext

from srai_telegrambot.telegram_bot_interface import TelegramBotInterface


class TextModeBase(ABC):

    def __init__(self, text_mode_name: str) -> None:
        self.text_mode_name = text_mode_name
        self.telegram_bot: TelegramBotInterface = None  # type: ignore

    def register(self, telegram_bot: TelegramBotInterface) -> None:
        if telegram_bot is None:
            raise ValueError("telegram_bot cannot be None")
        self.telegram_bot = telegram_bot

    def handle_text(self, update: Update, context: CallbackContext):
        if self.telegram_bot is None:
            raise ValueError("Cannot run unregistered text mode")
        message = self._handle_text(str(update.message.chat_id), update.message.text)
        update.message.reply_text(message)

    def try_load_mode_state(self, chat_id: str) -> Optional[dict]:
        state_id: str = self.text_mode_name + "_" + chat_id
        # make sha256 hash of state_id
        state_id_hash: str = hashlib.sha256(state_id.encode()).hexdigest()

        return self.telegram_bot.get_dao().try_load_mode_state(state_id_hash)

    def save_mode_state(self, chat_id: str, mode_state: dict):
        state_id: str = self.text_mode_name + "_" + chat_id
        # make sha256 hash of state_id
        state_id_hash: str = hashlib.sha256(state_id.encode()).hexdigest()
        return self.telegram_bot.get_dao().save_mode_state(state_id_hash, mode_state)

    @abstractmethod
    def _handle_text(self, chat_id: str, text: str) -> str:
        raise NotImplementedError()
