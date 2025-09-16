from abc import ABC, abstractmethod

from uuid import UUID

from api.model.audio_play import AudioPlay, AudioPlayLocation, \
    SearchAudioPlaysResponse
from api.model.error_response import ErrorResponse


class AudioPlayService(ABC):
    """Wrapper of audio play service API."""

    @abstractmethod
    def get(self, audio_play_id: UUID) -> AudioPlay | ErrorResponse | None:
        """
        Gets audio play by ID.
        :param audio_play_id: ID of an audio play.
        :return: audio play if success, error response
        from API, or None when couldn't get response.
        """
        pass

    @abstractmethod
    def search(
            self,
            query: str,
            limit: int | None = None
    ) -> SearchAudioPlaysResponse | ErrorResponse | None:
        """
        Searches audio plays by query string.
        :param query: query string.
        :param limit: max number of elements needed.
        :return: search response if success, error response
        from API, or None when couldn't get response.
        """
        pass

    @abstractmethod
    def get_location(
            self,
            token: str,
            audio_play_id: UUID
    ) -> AudioPlayLocation | ErrorResponse | None:
        """
        Gets self-hosted location of an audio play.
        :param token: token to authenticate with.
        :param audio_play_id: ID of an audio play.
        :return: location if success, error response
        from API, or None when couldn't get response.
        """
        pass
