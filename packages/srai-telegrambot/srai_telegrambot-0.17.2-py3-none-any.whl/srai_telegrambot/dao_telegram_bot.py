from typing import Dict, Optional

from srai_core.store.database_base import DatabaseBase
from srai_core.store.document_store_base import DocumentStoreBase
from srai_core.store.document_store_cached import DocumentStoreCached

from srai_telegrambot.model.chat_message import ChatMessage


class DaoTelegramBot:

    def __init__(self, database: DatabaseBase, cache_database=False) -> None:
        self.database = database
        self.list_document_store_name = [
            "skill_state",
            "mode_state",
            "chat_message",
        ]
        self.dict_document_store: Dict[str, DocumentStoreBase] = {}
        for name_store in self.list_document_store_name:
            if cache_database:
                self.dict_document_store[name_store] = DocumentStoreCached(database.get_document_store(name_store))
            else:
                self.dict_document_store[name_store] = database.get_document_store(name_store)

        self.store_skill_state = self.dict_document_store["skill_state"]
        self.store_mode_state = self.dict_document_store["mode_state"]
        self.store_chat_message = self.dict_document_store["chat_message"]

    def save_message(self, chat_message: ChatMessage) -> None:
        self.store_chat_message.save_document(chat_message.message_id, chat_message.to_dict())

    def save_skill_state(self, skill_state_id: str, skill_state: dict) -> None:
        self.store_skill_state.save_document(skill_state_id, skill_state)

    def load_skill_state(self, skill_state_id: str) -> dict:
        return self.store_skill_state.load_document(skill_state_id)

    def try_load_mode_state(self, mode_state_id: str) -> Optional[dict]:
        if not self.store_mode_state.exists_document(mode_state_id):
            return None
        return self.store_mode_state.load_document(mode_state_id)

    def save_mode_state(self, mode_state_id: str, mode_state: dict) -> None:
        self.store_mode_state.save_document(mode_state_id, mode_state)
