from adapters.handlers.utils.markdown import code, h1
from logics.bot import Bot
from logics.logic import Logic
from logics.message import BotMessage

_START = BotMessage(
    text="\n\n".join(
        x for x in (
            h1("dwtr Telegram bot"),

            "Helps you search audio plays, just type:\n" +
            code("/search whatever you want to find"),

            "Audio plays are being searched by title and synopsis. "
            "So if you want to quickly find an audio play, just type "
            "its title, but please be aware that only a small fraction "
            "of them has been added. More will come.",

            "Right now we only store original titles and synopsis. Localized "
            "versions will be added some time later.",

            "So type to start searching:\n" + code("/search doctor who")
        )
    )
)


class StartCommandHandler(Logic):
    """Handler of start command."""

    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot
    ) -> None:
        await bot.send_message(
            message=_START,
            user_id=user_id
        )
