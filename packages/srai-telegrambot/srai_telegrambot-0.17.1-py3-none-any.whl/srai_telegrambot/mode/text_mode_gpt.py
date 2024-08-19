from srai_openai.client_openai_chatgpt import ClientOpenaiChatgpt
from srai_openai.model.prompt_config import PromptConfig

from srai_telegrambot.mode.text_mode_base import TextModeBase


class TextModeGpt(TextModeBase):

    def __init__(self, system_message_content: str):
        super().__init__("text_mode_gpt")
        self.client = ClientOpenaiChatgpt()
        self.system_message_content = system_message_content

    def _handle_text(self, chat_id: str, prompt: str) -> str:
        mode_state = self.try_load_mode_state(chat_id)
        if mode_state is None:
            prompt_config = PromptConfig.create("gpt-4o", self.system_message_content)
        else:
            prompt_config = PromptConfig.from_dict(mode_state)
        prompt_config = prompt_config.append_user_message(prompt)
        prompt_config_result = self.client.prompt_for_prompt_config(prompt_config)
        self.save_mode_state(chat_id, prompt_config_result.to_dict())
        return prompt_config_result.last_message_text
