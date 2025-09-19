import logging

from adapters.handlers.error_response_handler import handle_error_response
from adapters.handlers.utils.audio_plays import make_starring, make_written_by
from adapters.handlers.utils.markdown import bold
from api.audio_play_service import AudioPlayService
from logics.bot import Bot
from logics.logic import Logic
from logics.message import BotButton, BotMessage
from api.model.audio_play import AudioPlay, SearchAudioPlaysResponse
from api.model.error_response import ErrorResponse

_NOT_FOUND = BotMessage(
    text="😇 Nothing is found. Try something else."
)
_INVALID_ARGUMENT = BotMessage(
    text="😁 Query was expected as parameter."
)


def _make_search_entry(num: int, audio_play: AudioPlay) -> str:
    """
    Makes single search entry.
    :param num: ordinal number.
    :param audio_play: audio play to show.
    :return: string block.
    """
    return "\n".join(
        x for x in
        (f"{num}. {bold(audio_play.title)}",
         make_written_by(audio_play.writers),
         make_starring(audio_play.cast))
        if x is not None
    )


def _make_search_message(r: SearchAudioPlaysResponse) -> BotMessage:
    """
    Makes message with search result.
    :param r: search response from API.
    :return: message to send to user.
    """
    if not r.audio_plays:
        return _NOT_FOUND

    text = []
    buttons = []
    for (i, audio_play) in enumerate(r.audio_plays):
        num = i + 1
        text.append(_make_search_entry(num, audio_play))
        buttons.append(BotButton(str(num), f"/get {audio_play.id}"))

    return BotMessage(
        text="\n\n".join(text),
        buttons=buttons
    )


class SearchAudioPlaysHandler(Logic):
    """Searches audio plays by query found in message."""

    def __init__(self, aps: AudioPlayService):
        """
        Constructor.
        :param aps: audio play service to make search calls to.
        """
        self._aps = aps

    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot
    ) -> None:
        if not message.text.strip():
            return await bot.send_message(
                message=_INVALID_ARGUMENT,
                user_id=user_id
            )
        
        match self._aps.search(message.text, 5):
            case SearchAudioPlaysResponse() as response:
                message = _make_search_message(response)
                logging.info(f"[{user_id}] <- {message}")
                return await bot.send_message(
                    message=message,
                    user_id=user_id
                )
            case ErrorResponse() as response:
                return await handle_error_response(user_id, response, bot)
            case _:
                return
