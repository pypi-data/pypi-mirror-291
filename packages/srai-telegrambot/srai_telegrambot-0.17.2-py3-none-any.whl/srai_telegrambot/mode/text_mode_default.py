from srai_telegrambot.mode.text_mode_base import TextModeBase


class ModeDefault(TextModeBase):
    def __init__(self):
        super().__init__("text_mode_default")

    def handle_text(self, update, context):
        update.message.reply_text(
            "Default mode is active and not specific text response will be given to non command messages."
        )
