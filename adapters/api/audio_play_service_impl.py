import requests_cache
from typing import Any
from urllib.parse import urlencode

from uuid import UUID
import logging

import requests

from api.audio_play_service import AudioPlayService
from api.model.audio_play import AudioPlay, AudioPlayLocation, \
    SearchAudioPlaysResponse
from api.model.error_response import ErrorResponse


class AudioPlayServiceImpl(AudioPlayService):
    """Service implementation."""

    def __init__(self, api_base: str):
        """
        Constructor.
        :param api_base: API base address.
        """
        self._base = api_base if api_base.endswith(
            "/") else api_base + "/"
        self._session = requests_cache.CachedSession(
            ".cache/audio_plays",
            expire_after=3600)

    def get(self, audio_play_id: UUID) -> AudioPlay | ErrorResponse | None:
        endpoint = self._base + f"audioPlays/{audio_play_id}"
        try:
            response = self._session.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                return AudioPlay(**data)
            elif response.content:
                data = response.json()
                return ErrorResponse(**data)
            else:
                return logging.warn("Received empty body.")
        except Exception:
            return logging.exception("Error while getting audio play.")

    def search(
            self,
            query: str,
            limit: int | None = None
    ) -> SearchAudioPlaysResponse | ErrorResponse | None:
        params = self._encode_params({
            "query": query,
            "limit": limit
        })
        endpoint = self._base + f"audioPlays:search?{params}"
        try:
            response = self._session.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                return SearchAudioPlaysResponse(**data)
            elif response.content:
                data = response.json()
                return ErrorResponse(**data)
            else:
                return logging.warn("Received empty body.")
        except Exception:
            return logging.exception("Error while searching audio plays.")

    def get_location(
            self,
            token: str,
            audio_play_id: UUID
    ) -> AudioPlayLocation | ErrorResponse | None:
        endpoint = self._base + f"audioPlays/{audio_play_id}/location"
        try:
            response = requests.get(endpoint, headers={
                "Authorization": f"Bearer {token}",
            })
            if response.status_code == 200:
                data = response.json()
                return AudioPlayLocation(**data)
            elif response.content:
                data = response.json()
                return ErrorResponse(**data)
            else:
                return logging.warn("Received empty body.")
        except Exception:
            return logging.exception("Error while getting audio play location.")

    @staticmethod
    def _encode_params(params: dict[str, Any]) -> str:
        """
        Encodes dictionary as URL params. Filters out Nones.
        :param params: params as dict.
        :return: encoded string.
        """
        filtered = {
            key: value
            for key, value in params.items()
            if value is not None
        }
        return urlencode(filtered)
