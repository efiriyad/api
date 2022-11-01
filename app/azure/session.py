import logging

from azure.storage.blob import BlobServiceClient

from app.core import settings

log = logging.getLogger(__name__)

azure = BlobServiceClient.from_connection_string(settings.azure.connection_string)
log.info("Initialized Azure blob session")
