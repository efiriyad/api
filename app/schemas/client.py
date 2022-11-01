from pydantic import BaseModel

from app.core import settings


class ClientCreate(BaseModel):
    """The client response."""

    token: str


class Client(BaseModel):
    """The client response."""

    profile: dict[str, str] = {
        "name": "",
        "picture": f"{settings.site.cdn}/images/profile/default.png"
    }

    notifications: dict[str, dict] = {
        "email": {"enabled": False, "address": ""},
        "push": {"enabled": False, "token": ""},
    }


class ClientPicture(BaseModel):
    """The client response."""

    url: str
