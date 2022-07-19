from typing import Generator

from pronotepy.exceptions import ENTLoginError

from app.firebase.session import db
from app.pronote.session import client as pronote_client


def get_db() -> Generator:
    """Returns a db instance."""
    yield db


def get_pronote() -> Generator:
    """Returns a pronote client instance."""
    if pronote_client.logged_in:
        yield pronote_client
    else:
        raise ENTLoginError("Pronote client is not logged in.")
