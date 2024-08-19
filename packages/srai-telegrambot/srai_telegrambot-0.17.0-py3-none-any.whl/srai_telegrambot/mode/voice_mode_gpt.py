import hashlib
import os

from srai_openai.client_openai_audio import ClientOpenaiAudio
from srai_openai.client_openai_chatgpt import ClientOpenaiChatgpt
from srai_openai.model.prompt_config import PromptConfig

from srai_telegrambot.mode.voice_mode_base import VoiceModeBase


class VoiceModeGpt(VoiceModeBase):

    def __init__(self, system_message_content) -> None:
        super().__init__("text_mode_gpt")
        self.client_chatgtpt = ClientOpenaiChatgpt()
        self.client_audio = ClientOpenaiAudio()
        self.system_message_content = system_message_content

    def _handle_voice(self, chat_id: str, voice_bytes: bytes, voice_bytes_format: str) -> str:
        instance_id = hashlib.sha256(voice_bytes).hexdigest()
        path_file_audio = instance_id + ".ogg"
        with open(path_file_audio, "wb") as f:
            f.write(voice_bytes)
        transcription = self.client_audio.transcription(path_file_audio)
        os.remove(path_file_audio)
        print()
        mode_state = self.try_load_mode_state(chat_id)
        if mode_state is None:
            prompt_config = PromptConfig.create("gpt-4o", self.system_message_content)
        else:
            prompt_config = PromptConfig.from_dict(mode_state)
        prompt_config = prompt_config.append_user_message(transcription["text"])
        prompt_config_result = self.client_chatgtpt.prompt_for_prompt_config(prompt_config)
        self.save_mode_state(chat_id, prompt_config_result.to_dict())
        return prompt_config_result.last_message_text
