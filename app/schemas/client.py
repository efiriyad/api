from pydantic import BaseModel


class ClientCreate(BaseModel):
    """The client response."""

    token: str


class Client(BaseModel):
    """The client response."""

    name: str = ""
    notifications: dict[str, dict] = {
        "email": {"enabled": False, "address": ""},
        "push": {"enabled": False, "token": ""},
    }
