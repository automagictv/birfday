import pytest
import telegram

from birfday import telegram_helper


class TestTelegramHelper:

    def test_helper_gets_bot_client(self, mocker):
        """Tests that the constructor retrieves a bot client."""
        mocker.patch.object(
            telegram_helper,
            "Bot",
            autospec=True
        )
        fkey = "FAKEKEY"
        fid = "FAKEID"

        _ = telegram_helper.TelegramFacade(token=fkey, cid=fid)
        telegram_helper.Bot.assert_called_once_with(fkey)

    def test_send_message_calls_bot_send_message(self, mocker):
        """Tests that we call the Bot.send_message method to send."""
        mocker.patch.object(
            telegram_helper,
            "Bot",
            autospec=True
        )

        fkey = "FAKEKEY"
        fid = "FAKEID"
        fkmsg = "FAKEMESSAGE"

        helper = telegram_helper.TelegramFacade(token=fkey, cid=fid)
        helper.send_message(fkmsg)

        helper.client.send_message.assert_called_once_with(
            fid,
            fkmsg,
            telegram.ParseMode.HTML
        )
