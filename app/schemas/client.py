from pydantic import BaseModel


class ClientCreate(BaseModel):
    """The client response."""

    token: str


class Client(BaseModel):
    """The client response."""

    profile: dict[str, str] = {
        "name": "",
        "picture": "https://cdn.efiriyad.tech/images/profile/default.png"
    }

    notifications: dict[str, dict] = {
        "email": {"enabled": False, "address": ""},
        "push": {"enabled": False, "token": ""},
    }
