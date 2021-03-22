import telegram

from birfday import config


class TelegramFacade(object):

    def __init__(self, token=config.TELEGRAM_TOKEN,
                 cid=config.TELEGRAM_CHAT_ID):
        pass

    def send_message(self, message):
        """Sends a markdown message to our telegram user.

        Args:
            message: String, markdown representing a message to send.
        Returns:
            Telegram response object.
        """
        raise NotImplementedError
