import enum

from pydantic import BaseModel


class OAuth2Provider(enum.StrEnum):
    """Provider of OAuth services."""
    GOOGLE = "google"


class BasicAuthentication(BaseModel):
    """
    Authentication request via username and password
    :param username: username.
    :param password: password.
    """
    username: str
    password: str

    def model_dump(self, *args, **kwargs) -> dict:
        return {"basic": super().model_dump(*args, **kwargs)}

    def model_dump_json(self, *args, **kwargs) -> str:
        import json
        return json.dumps(self.model_dump(*args, **kwargs))


class OAuth2Authentication(BaseModel):
    """
    Authentication request via external service
    :param provider: OAuth service provider.
    :param authorization_code: code received from them.
    """
    provider: OAuth2Provider
    authorization_code: str

    def model_dump(self, *args, **kwargs) -> dict:
        return {"oauth2": super().model_dump(*args, **kwargs)}

    def model_dump_json(self, *args, **kwargs) -> str:
        import json
        return json.dumps(self.model_dump(*args, **kwargs))


class AuthenticateUserResponse(BaseModel):
    """
    Positive authentication response.
    :param access_token: access token.
    :param id_token: ID token.
    """
    access_token: str
    id_token: str


class CreateUserRequest(BaseModel):
    """
    Request to register new user.
    :param username: chosen username.
    :param oauth2: OAuth2 information from external service.
    """
    username: str
    oauth2: OAuth2Authentication


AuthenticateUserRequest = BasicAuthentication | OAuth2Authentication
