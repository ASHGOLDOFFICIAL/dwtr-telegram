import logging

import requests
from uuid import UUID

from typing import Sequence

from adapters.handlers.error_response_handler import handle_error_response
from adapters.handlers.utils.audio_plays import make_starring, make_written_by
from adapters.handlers.utils.markdown import HORIZONTAL_RULE, bold, h1, h2, \
    italic, \
    link
from api.audio_play_service import AudioPlayService
from api.tokens import TokenStore
from logics.bot import Bot
from logics.logic import Logic
from logics.message import BotMessage
from api.model.audio_play import AudioPlay, AudioPlayLocation, CastMember
from api.model.error_response import ErrorResponse
from api.model.external_resource import ExternalResource

_NOT_UUID = BotMessage(
    text="UUID was expected."
)

_BLOCK_SEPARATOR = HORIZONTAL_RULE + "\n"


def _make_series_info(audio_play: AudioPlay) -> str | None:
    """
    Makes series info line with series name, season and number.
    :rtype: str | None line if series is given, otherwise None. 
    """
    els = [audio_play.series_season, audio_play.series_number]
    number = ".".join(str(x) for x in els if x is not None)
    return " ".join((audio_play.series.name, number))


def _make_resources(res: Sequence[ExternalResource]) -> Sequence[str]:
    """
    Makes resources block for a message.
    :param res: resources to display.
    :return: resources block lines or None if no resources are given.
    """
    return [f"{r.resource_type}: {link("link", r.link)}" for r in res]


def _make_cast(cast: Sequence[CastMember]) -> Sequence[str]:
    """
    Makes cast block for a message.
    :param cast: cast to display.
    :return: block lines or None if cast is empty.
    """
    sorted_cast: Sequence[CastMember] = sorted(cast, key=lambda m: not m.main)

    def _make_entry(c: CastMember) -> str:
        roles = " / ".join(c.roles)
        return f"{bold(c.actor.name)} ({roles})"

    return [_make_entry(m) for m in sorted_cast]


def _get_cover(cover_uri: str) -> bytes | None:
    """
    Retrieves cover by URI.
    :rtype: bytes | None cover as bytes if success, otherwise None.
    """
    response = requests.get(cover_uri)
    if response.status_code == 200:
        image_data = response.content
        return image_data
    return None


def _make_card_message(audio_play: AudioPlay) -> BotMessage:
    """
    Makes audio play card message, i.e. cover with basic info.
    :param audio_play: audio play to make card of.
    :return: bot message.
    """
    cover = _get_cover(audio_play.cover_uri) if audio_play.cover_uri else None
    series_info = _make_series_info(audio_play)
    written_by = make_written_by(audio_play.writers)
    starring = make_starring(audio_play.cast)
    released = italic(
        f"Released: {audio_play.release_date.strftime("%B %d, %Y")}"
    )
    card_lines = (
        h1(audio_play.title),
        "",
        series_info,
        written_by,
        starring,
        released,
    )
    text = "\n".join(x for x in card_lines if x is not None)
    return BotMessage(text=text, image=cover)


def _make_details_message(
        audio_play: AudioPlay,
        location: str | None
) -> BotMessage | None:
    """
    Makes message with audio play details like
    synopsis, cast and external resources.
    :rtype: BotMessage | None bot message if any of
    the above is present, otherwise None.
    """
    cast = _make_cast(audio_play.cast)
    resources = [
        x for x in
        (
            *_make_resources(audio_play.external_resources),
            f"self-hosted: {link("link", location)}" if location else None,
        ) if x is not None
    ]

    blocks = filter(lambda x: x is not None, (
        (h2("Synopsis") + "\n" + audio_play.synopsis)
        if audio_play.synopsis else None,

        (h2("Cast") + "\n" + "\n".join(cast))
        if cast else None,

        (h2("Links") + "\n" + "\n".join(resources))
        if resources else None
    ))
    text = _BLOCK_SEPARATOR.join(blocks)
    return BotMessage(text=text) if text else None


class GetAudioPlayHandler(Logic):
    """Displays one audio play found by ID in message."""

    def __init__(self, aps: AudioPlayService, ts: TokenStore):
        """
        Constructor.
        :param aps: audio play service to make search calls to.
        :param ts: token store to get user tokens from.
        """
        self._aps = aps
        self._ts = ts

    async def process_message(
            self,
            user_id: int,
            message: BotMessage,
            bot: Bot
    ) -> None:
        guid: UUID
        try:
            guid = UUID(message.text)
        except ValueError:
            return await bot.send_message(
                message=_NOT_UUID,
                user_id=user_id)

        match self._aps.get(guid):
            case AudioPlay() as audio_play:
                location = self._get_location(user_id, guid)
                await bot.send_message(
                    message=_make_card_message(audio_play),
                    user_id=user_id
                )
                details = _make_details_message(audio_play, location)
                return await bot.send_message(
                    message=details,
                    user_id=user_id
                ) if details else None
            case ErrorResponse() as response:
                return await handle_error_response(user_id, response, bot)
            case _:
                return

    def _get_location(self, user_id: int, guid: UUID) -> str | None:
        """
        Gets self-hosted location from service.
        :param user_id: ID of user who performs this action.
        :param guid: ID of an audio play.
        :return: string if found, otherwise None.
        """
        token = self._ts.get(user_id)
        if token:
            response = self._aps.get_location(token, guid)
            if isinstance(response, AudioPlayLocation):
                logging.info(f"Received self-hosted location of {guid}")
                return response.uri
        return None
