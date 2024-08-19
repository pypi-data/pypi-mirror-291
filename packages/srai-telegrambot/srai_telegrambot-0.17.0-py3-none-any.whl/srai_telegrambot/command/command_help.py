from srai_telegrambot.command.command_base import CommandBase


class CommandHelp(CommandBase):
    def __init__(self):
        super().__init__("help")

    def execute_command(self, chat_id: str, command_message: str) -> None:
        """Send a message when the command /help is issued."""
        message = "Available commands:\n"
        for command in self.telegram_bot.dict_command.keys():  # type: ignore
            message += f"/{command}\n"
        self.telegram_bot.message_chat(chat_id, message)
