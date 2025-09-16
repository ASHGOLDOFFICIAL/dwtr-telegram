from api.tokens import TokenStore
from logics.bot import Bot
from logics.logic import Logic
from logics.message import BotMessage

_NOT_FOUND = BotMessage(
    text="No token is found."
)


class TokenCommandHandler(Logic):
    """Handler of token command."""

    def __init__(self, ts: TokenStore):
        """
        Constructor.
        :param ts: token store to check for tokens.
        """
        self._ts = ts

    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot
    ) -> None:
        token = self._ts.get(user_id)
        if token:
            return await bot.send_message(
                message=BotMessage(text=token),
                user_id=user_id
            )
        return await bot.send_message(
            message=_NOT_FOUND,
            user_id=user_id
        )
