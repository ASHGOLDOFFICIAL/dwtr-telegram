from logics.bot import Bot
from logics.logic import Logic
from logics.message import BotMessage

_UNKNOWN_COMMAND = BotMessage(
    text="Unknown command."
)


class UnknownCommandHandler(Logic):
    """Handler of unknown command."""

    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot
    ) -> None:
        await bot.send_message(
            message=_UNKNOWN_COMMAND,
            user_id=user_id
        )
