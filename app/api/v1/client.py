import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from google.cloud import firestore

from app.api.deps import get_db
from app.schemas import Client, ClientCreate

log = logging.getLogger(__name__)
router = APIRouter()


@router.post("", response_model=ClientCreate)
def create_client(db: firestore.Client = Depends(get_db)) -> Any:
    """Create a new client and return its UUID."""
    _, client_ref = db.collection("clients").add({
        "profile": {
            "name": "",
            "picture": "https://cdn.efiriyad.tech/images/profile/default.png"
        },
        "notifications": {
            "email": {"enabled": False, "address": ""},
            "push": {"enabled": False, "token": ""},
        }
    })

    return {"token": client_ref.id}


@router.get("", response_model=Client)
def get_client(token: str, db: firestore.Client = Depends(get_db)) -> Any:
    """Fetch a client and return its data."""
    client_ref = db.collection("clients").document(token)
    client = client_ref.get()

    if client.exists:
        return client.to_dict()

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The client with this token does not exist in the system.",
    )


@router.put("", status_code=status.HTTP_200_OK, response_class=Response)
def update_client(token: str, data: Client, db: firestore.Client = Depends(get_db)) -> Any:
    """Update a specific client's data."""
    client_ref = db.collection("clients").document(token)
    client = client_ref.get()

    if client.exists:
        client_ref.update(data.dict())
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The client with this token does not exist in the system.",
    )
