from abc import ABC, abstractmethod
import logging
import requests

from api.authentication_service import AuthenticationService
from api.model.authentication import AuthenticateUserRequest, \
    AuthenticateUserResponse, CreateUserRequest
from api.model.error_response import ErrorResponse


class AuthenticationServiceImpl(AuthenticationService):
    """Service implementation."""

    def __init__(self, api_base: str):
        """
        Constructor.
        :param api_base: API base address.
        """
        self._base = api_base if api_base.endswith(
            "/") else api_base + "/"

    def login(
            self,
            request: AuthenticateUserRequest
    ) -> AuthenticateUserResponse | ErrorResponse | None:
        endpoint = self._base + f"users:authenticate"
        try:
            response = requests.post(endpoint, json=request.model_dump())
            if response.status_code == 200:
                data = response.json()
                return AuthenticateUserResponse(**data)
            elif response.content:
                data = response.json()
                return ErrorResponse(**data)
            else:
                return logging.warn("Received empty body.")
        except Exception:
            return logging.exception("Error while log in.")

    def register(
            self,
            request: CreateUserRequest,
    ) -> AuthenticateUserResponse | ErrorResponse | None:
        endpoint = self._base + f"users"
        try:
            response = requests.post(endpoint, json=request.model_dump())
            if response.status_code == 201:
                data = response.json()
                return AuthenticateUserResponse(**data)
            elif response.content:
                data = response.json()
                return ErrorResponse(**data)
            else:
                return logging.warn("Received empty body.")
        except Exception:
            return logging.exception("Error while registering.")
