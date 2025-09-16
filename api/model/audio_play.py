import enum

from pydantic import BaseModel
from datetime import date

from uuid import UUID

from api.model.external_resource import ExternalResource
from api.model.language import Language
from api.model.person import Person


class CastMember(BaseModel):
    """
    Cast member.
    :param actor: actor person.
    :param roles: roles played by this actor in this audio play.
    :param main: whether actor is part of main class.
    """
    actor: Person
    roles: list[str]
    main: bool


class AudioPlaySeries(BaseModel):
    """
    Audio play series.
    :param id: ID of the series.
    :param name: series name.
    """
    id: UUID
    name: str


class AudioPlayTranslationType(enum.StrEnum):
    """Type of audio play translation."""
    TRANSCRIPT = "transcript"
    SUBTITLES = "subtitles"
    VOICEOVER = "voiceover"


class AudioPlayTranslation(BaseModel):
    """
    Audio play translation.
    :param original_id: ID of the original audio play.
    :param id: ID of this translation.
    :param title: translated title.
    :param translation_type: type of this translation.
    :param language: language of translation.
    :param external_resources: links to external resources.
    """
    original_id: UUID
    id: UUID
    title: str
    translation_type: AudioPlayTranslationType
    language: Language
    external_resources: list[ExternalResource]


class AudioPlay(BaseModel):
    """
    Audio play.
    :param id: ID of an audio play.
    :param title: title.
    :param synopsis: synopsis.
    :param release_date: release date.
    :param writers: writers of this audio play.
    :param cast: audio play cast.
    :param series: series this audio play belongs to.
    :param series_season: season of this audio play.
    :param series_number: number in season/series.
    :param cover_uri: URI to cover.
    :param external_resources: links to external resources.
    """
    id: UUID
    title: str
    synopsis: str
    release_date: date
    writers: list[Person]
    cast: list[CastMember]
    series: AudioPlaySeries | None
    series_season: int | None
    series_number: int | None
    cover_uri: str | None
    external_resources: list[ExternalResource]


class SearchAudioPlaysResponse(BaseModel):
    """Response to search request."""
    audio_plays: list[AudioPlay]


class AudioPlayLocation(BaseModel):
    """Self-hosted location of an audio play."""
    uri: str
