import logging

from adapters.handlers.get_audio_play import GetAudioPlayHandler
from adapters.handlers.login_handler import LoginCommandHandler
from adapters.handlers.search_audio_plays import SearchAudioPlaysHandler
from adapters.handlers.start_handler import StartCommandHandler
from adapters.handlers.token_handler import TokenCommandHandler
from adapters.handlers.unknown_handler import UnknownCommandHandler
from api.authentication_service import AuthenticationService
from api.tokens import TokenStore
from logics.bot import Bot
from logics.logic import Logic
from logics.message import BotMessage
from api.audio_play_service import AudioPlayService

_INVALID_REQUEST = BotMessage(
    text="Empty messages are not allowed."
)


class LogicImpl(Logic):
    """dwtr bot logic."""

    def __init__(
            self,
            aus: AuthenticationService,
            aps: AudioPlayService,
            ts: TokenStore,
    ):
        """
        Constructor.
        :param aus: authentication service to use.
        :param aps: audio play service.
        :param ts: place to store tokens.
        """
        self._start_handler = StartCommandHandler()
        self._login_handler = LoginCommandHandler(aus, ts)
        self._token_handler = TokenCommandHandler(ts)
        self._search_handler = SearchAudioPlaysHandler(aps)
        self._get_handler = GetAudioPlayHandler(aps, ts)
        self._unknown_handler = UnknownCommandHandler()

    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot
    ) -> None:
        logging.info(f"[{user_id}] -> {message}")
        text = message.text
        if not text:
            return await bot.send_message(_INVALID_REQUEST, user_id)

        parts = message.text.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        handler = self._choose_handler(command)
        try:
            return await handler.process_message(
                user_id, BotMessage(text=args), bot
            )
        except Exception:
            logging.exception(
                f"Handler {handler.__class__.__name__} threw error."
            )
            return None

    def _choose_handler(self, command: str) -> Logic:
        """
        Chooses handler based on command.
        :param command: received command.
        """
        match command.lower():
            case "/login":
                return self._login_handler
            case "/token":
                return self._token_handler
            case "/search":
                return self._search_handler
            case "/get":
                return self._get_handler
            case '/start':
                return self._start_handler
            case _:
                return self._unknown_handler
    