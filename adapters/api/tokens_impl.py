import logging

from api.tokens import TokenStore

import jwt
from datetime import datetime, timezone


def _is_expired(token: str) -> bool:
    """
    Checks token expiration.
    :param token: JWT token to check.
    :return: `True` if expired.
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")
        if exp is not None:
            return datetime.now(timezone.utc).timestamp() >= exp
        return True
    except jwt.DecodeError:
        logging.error("Invalid token was stored.")
        return True


class DictTokenStore(TokenStore):
    """Token store implementation via dict."""

    def __init__(self):
        """Constructor."""
        self._dict = {}

    def get(self, user_id: int) -> str | None:
        token = self._dict.get(user_id)
        if not token or _is_expired(token):
            return None
        return token

    def put(self, user_id: int, token: str) -> None:
        self._dict[user_id] = token
