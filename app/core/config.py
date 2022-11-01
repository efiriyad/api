from pydantic import BaseSettings


class API(BaseSettings):
    """The API settings."""

    name: str = "Efiriyad"
    endpoint: str = "/api/v1"

    host: str = "0.0.0.0"
    port: int = 8080

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "API_"


class Azure(BaseSettings):
    """The Firebase settings."""

    connection_string: str

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "AZURE_"


class FireBase(BaseSettings):
    """The Firebase settings."""

    project_id: str
    private_key: str
    client_email: str

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "FIREBASE_"


class Config(BaseSettings):
    """The application settings."""

    timezone: str = "Asia/Riyadh"
    day_start: str = "07:45"
    day_end: str = "17:30"
    lesson_duration: int = 55  # In minutes.

    backup_years: str = "2021-2022"

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "APP_"


class Global(BaseSettings):
    """The app settings."""

    api: API = API()
    azure: Azure = Azure()
    firebase: FireBase = FireBase()

    # This key will be used to decrypt the user passwords stored in the
    # users -> user -> password firestore field.
    password_key: str

    debug: bool = False

    class Config:
        """The Pydantic settings configuration."""

        env_file = ".env"


settings = Global()

# Replace /n with real new lines (For fly.io environments).
settings.firebase.project_id = settings.firebase.project_id.replace("\\n", "\n").replace("\\t", "\t")
settings.firebase.private_key = settings.firebase.private_key.replace("\\n", "\n").replace("\\t", "\t")
settings.firebase.client_email = settings.firebase.client_email.replace("\\n", "\n").replace("\\t", "\t")
config = Config()
