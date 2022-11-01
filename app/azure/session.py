import logging
import sys

from azure.storage.blob import BlobServiceClient

from app.core import settings

log = logging.getLogger(__name__)

if "pytest" in sys.modules:
    # This is a pytest environment.
    azure = None
else:
    azure = BlobServiceClient.from_connection_string(settings.azure.connection_string)
    log.info("Initialized Azure blob session")
