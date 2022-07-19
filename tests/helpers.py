from unittest import mock


class Mock(mock.Mock):
    """Custom Mock class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MockSubject:
    """Mock a subject with a name attribute."""

    def __init__(self, name: str):
        self.name = name
