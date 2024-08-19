import os

from srai_telegrambot.command.command_base import CommandBase


def get_image_tag():
    image_tag = os.environ.get("IMAGE_TAG")
    if image_tag is None:
        message = "IMAGE_TAG not set"
    else:
        message = f"{image_tag}"
    return message


class CommandImageTag(CommandBase):
    def __init__(self):
        super().__init__("image_tag")

    def execute_command(self, chat_id: str, command_message: str) -> None:
        """Send a message when the command /help is issued."""
        image_tag = get_image_tag()
        self.telegram_bot.message_chat(chat_id, f"image tag running:  {image_tag}")
