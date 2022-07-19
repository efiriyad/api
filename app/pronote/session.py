import logging
import sys

import pronotepy
from cryptography.fernet import Fernet

from app.core import settings
from app.firebase.session import db

log = logging.getLogger(__name__)

if "pytest" in sys.modules:
    client = pronotepy.Client(
        "https://demo.index-education.net/pronote/eleve.html",
        username="demonstration",
        password="pronotevs",
    )
else:
    # Get all the users in the users collection.
    user_docs = db.collection("users").get()
    users = [user.to_dict() for user in user_docs]

    log.info(f"Found {len(users)} pronote user accounts")
    cipher = Fernet(settings.password_key)

    clients = []
    for user in users:
        # Get the url, username and decrypt the password.
        url = user["pronote"]["url"]
        username = user["pronote"]["username"]
        password = cipher.decrypt(user["pronote"]["password"].encode()).decode()

        client = pronotepy.Client(url, username, password)
        clients.append(client)

        log.info(f"Initialized pronote client for {username}")

    client = clients[0]
