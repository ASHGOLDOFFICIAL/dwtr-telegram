from abc import ABC, abstractmethod

from api.model.authentication import AuthenticateUserRequest, \
    AuthenticateUserResponse, CreateUserRequest
from api.model.error_response import ErrorResponse


class AuthenticationService(ABC):
    """Wrapper of authentication service API."""

    @abstractmethod
    def login(
            self,
            request: AuthenticateUserRequest
    ) -> AuthenticateUserResponse | ErrorResponse | None:
        """
        Authenticate user by given credentials.
        :param request: request with credentials.
        :return: response with tokens if success, error response
        if service returned error, or None if no response was received.
        """
        pass

    @abstractmethod
    def register(
            self,
            request: CreateUserRequest,
    ) -> AuthenticateUserResponse | ErrorResponse | None:
        """
        Registers new user.
        :param request: request with registration details.
        :return: response with tokens if success, error response
        if service returned error, or None if no response was received.
        """
        pass
