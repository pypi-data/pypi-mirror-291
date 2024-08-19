from srai_telegrambot.command.command_base import CommandBase


class CommandChatId(CommandBase):
    def __init__(self):
        super().__init__("chat_id")

    def execute_command(self, chat_id: str, command_message: str) -> None:
        """Send a message when the command /help is issued."""
        self.telegram_bot.message_chat(chat_id, f"Chat id of this chat  {chat_id}")
