from abc import ABC, abstractmethod


class TokenStore(ABC):
    """Storage for user tokens received from API."""

    @abstractmethod
    def get(self, user_id: int) -> str | None:
        """
        Gets stored access token for user.
        :param user_id: user ID.
        :return: access token if found and not expired.
        """
        pass

    @abstractmethod
    def put(self, user_id: int, token: str) -> None:
        """
        Puts token for given user.
        :param user_id: user for whom to save this token.
        :param token: access token to save.
        """
        pass
