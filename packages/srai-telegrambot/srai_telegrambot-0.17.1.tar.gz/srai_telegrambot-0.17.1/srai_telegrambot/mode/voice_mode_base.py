import hashlib
from abc import ABC, abstractmethod
from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext

from srai_telegrambot.telegram_bot_interface import TelegramBotInterface


class VoiceModeBase(ABC):

    def __init__(self, voice_mode_name: str) -> None:
        self.voice_mode_name = voice_mode_name
        self.telegram_bot: TelegramBotInterface = None  # type: ignore

    def register(self, telegram_bot: TelegramBotInterface) -> None:
        if telegram_bot is None:
            raise ValueError("telegram_bot cannot be None")
        self.telegram_bot = telegram_bot

    def handle_voice(self, update: Update, context: CallbackContext):
        if self.telegram_bot is None:
            raise ValueError("Cannot run unregistered text mode")
        voice_bytes = update.message.voice.get_file().download_as_bytearray()
        voice_bytes_format = "audio/ogg"
        message = self._handle_voice(str(update.message.chat_id), voice_bytes, voice_bytes_format)
        update.message.reply_text(message)

    def try_load_mode_state(self, chat_id: str) -> Optional[dict]:
        state_id: str = self.voice_mode_name + "_" + chat_id
        # make sha256 hash of state_id
        state_id_hash: str = hashlib.sha256(state_id.encode()).hexdigest()
        return self.telegram_bot.get_dao().try_load_mode_state(state_id_hash)

    def save_mode_state(self, chat_id: str, mode_state: dict):
        state_id: str = self.voice_mode_name + "_" + chat_id
        # make sha256 hash of state_id
        state_id_hash: str = hashlib.sha256(state_id.encode()).hexdigest()
        return self.telegram_bot.get_dao().save_mode_state(state_id_hash, mode_state)

    @abstractmethod
    def _handle_voice(self, chat_id: str, text: str) -> str:
        raise NotImplementedError()
