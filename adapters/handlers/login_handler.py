import logging

from adapters.handlers.error_response_handler import handle_error_response
from api.authentication_service import AuthenticationService
from api.model.authentication import \
    AuthenticateUserResponse, BasicAuthentication
from api.model.error_response import ErrorResponse
from api.tokens import TokenStore
from logics.bot import Bot
from logics.logic import Logic
from logics.message import BotMessage

_INVALID_ARGUMENTS = BotMessage(
    text="Invalid arguments, "
         "two arguments are expected: "
         "username and password."
)


class LoginCommandHandler(Logic):
    """Handler of login command."""

    def __init__(self, aus: AuthenticationService, ts: TokenStore):
        """
        Constructor.
        :param aus: authentication service to use.
        :param ts: place to store tokens.
        """
        self._aus = aus
        self._ts = ts

    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot
    ) -> None:
        args: list[str] = message.text.split()
        if len(args) != 2:
            return await bot.send_message(
                message=_INVALID_ARGUMENTS,
                user_id=user_id
            )

        request = BasicAuthentication(username=args[0], password=args[1])
        match self._aus.login(request):
            case AuthenticateUserResponse() as response:
                self._ts.put(user_id, response.access_token)
                message = BotMessage(text="Success!")
                logging.info(f"[{user_id}] <- {message}")
                return await bot.send_message(
                    message=message,
                    user_id=user_id)
            case ErrorResponse() as response:
                return await handle_error_response(user_id, response, bot)
            case _:
                return
