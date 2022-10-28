from datetime import datetime
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tests.helpers import Mock, MockSubject

from app.__main__ import app
from app.firebase.session import db


@pytest.fixture(scope="session")
def get_db() -> Generator:
    """Return a database instance."""
    yield db


@pytest.fixture(scope="module")
def client() -> Generator:
    """Return the test client."""
    with TestClient(app) as c:
        yield c


# Schedules examples.
@pytest.fixture(scope="module")
def wednesday_schedule() -> list[Mock]:
    """Returns an example of a schedule."""
    # 2022-05-25
    return [
        Mock(
            background_color="#FFFF00",
            classrooms=["07"],
            end=datetime(2022, 5, 25, 9, 40),
            group_names=[],
            start=datetime(2022, 5, 25, 7, 45),
            status=None,
            subject=MockSubject("MATHÉMATIQUES"),
            teacher_names=["BELHADJ N."],
            canceled=False,
        ),
        Mock(
            background_color="#FF0080",
            classrooms=["07"],
            end=datetime(2022, 5, 25, 10, 50),
            group_names=[],
            start=datetime(2022, 5, 25, 9, 55),
            status=None,
            subject=MockSubject("ANGLAIS"),
            teacher_names=["HAFIDI M."],
            canceled=False,
        ),
        Mock(
            background_color="#0080FF",
            classrooms=["06"],
            end=datetime(2022, 5, 25, 11, 50),
            group_names=[],
            start=datetime(2022, 5, 25, 10, 55),
            status="Cours déplacé",
            subject=MockSubject("FRANÇAIS"),
            teacher_names=["DJERAD K."],
            canceled=False,
        ),
        Mock(
            background_color="#75B951",
            classrooms=["13"],
            end=datetime(2022, 5, 25, 12, 45),
            group_names=["[2 SL G1]"],
            start=datetime(2022, 5, 25, 11, 50),
            status=None,
            subject=MockSubject("SCIENCES & LABO"),
            teacher_names=["SAAB M."],
            canceled=False,
        ),
        Mock(
            background_color="#FF8080",
            classrooms=["05"],
            end=datetime(2022, 5, 25, 13, 40),
            group_names=[],
            start=datetime(2022, 5, 25, 12, 45),
            status="Prof. absent",
            subject=MockSubject("SC. ECO & SOC."),
            teacher_names=["BEN OTHMAN N."],
            canceled=True,
        ),
        Mock(
            background_color="#800000",
            classrooms=["211 - Info"],
            end=datetime(2022, 5, 25, 14, 35),
            group_names=[],
            start=datetime(2022, 5, 25, 13, 40),
            status="Changement de salle",
            subject=MockSubject("ACC PERSO"),
            teacher_names=["BELHADJ N."],
            canceled=False,
        ),
        Mock(
            background_color="#800000",
            classrooms=["10"],
            end=datetime(2022, 5, 25, 14, 35),
            group_names=["211 - Info"],
            start=datetime(2022, 5, 25, 13, 40),
            status="Cours annulé",
            subject=MockSubject("ACC PERSO"),
            teacher_names=["BELHADJ N."],
            canceled=True,
        ),
        Mock(
            background_color="#0080FF",
            classrooms=["06"],
            end=datetime(2022, 5, 25, 15, 35),
            group_names=[],
            start=datetime(2022, 5, 25, 14, 40),
            status="Cours annulé",
            subject=MockSubject("FRANÇAIS"),
            teacher_names=["DJERAD K."],
            canceled=True,
        )
    ]


@pytest.fixture(scope="module")
def thursday_schedule() -> list[Mock]:
    """Returns an example of a schedule."""
    # 2022-05-19
    return [
        Mock(
            background_color="#C0C0C0",
            classrooms=[],
            end=datetime(2022, 5, 25, 15, 35),
            group_names=[],
            start=datetime(2022, 5, 25, 7, 45),
            status="Exceptionnel",
            subject=MockSubject("ED.PHYSIQUE & SPORT."),
            teacher_names=["NEGHNAGH N.", "SAADOUNE S.", "CATRY V.", "DRIDI M."],
            canceled=False
        ),
        Mock(
            background_color="#0080FF",
            classrooms=["06"],
            end=datetime(2022, 5, 25, 8, 40),
            group_names=[],
            start=datetime(2022, 5, 25, 7, 45),
            status="Cours annulé",
            subject=MockSubject("FRANÇAIS"),
            teacher_names=["DJERAD K."],
            canceled=True,
        ),
        Mock(
            background_color="#EC6719",
            classrooms=[],
            end=datetime(2022, 5, 25, 9, 40),
            group_names=["[2 ALLD LVB]"],
            start=datetime(2022, 5, 25, 8, 45),
            status="Cours annulé",
            subject=MockSubject("ALLEMAND"),
            teacher_names=["SAKR S."],
            canceled=True,
        ),
        Mock(
            background_color="#00FF40",
            classrooms=["121"],
            end=datetime(2022, 5, 25, 10, 50),
            group_names=["[2AP.2]"],
            start=datetime(2022, 5, 25, 9, 55),
            status="Cours annulé",
            subject=MockSubject("SC. de la VIE & de la TERRE"),
            teacher_names=["SEMAAN F."],
            canceled=True,
        ),
        Mock(
            background_color="#0080FF",
            classrooms=["06"],
            end=datetime(2022, 5, 25, 12, 45),
            group_names=[],
            start=datetime(2022, 5, 25, 11, 50),
            status="Cours annulé",
            subject=MockSubject("FRANÇAIS"),
            teacher_names=["DJERAD K."],
            canceled=True,
        ),
        Mock(
            background_color="#FF0000",
            classrooms=["05"],
            end=datetime(2022, 5, 25, 13, 40),
            group_names=[],
            start=datetime(2022, 5, 25, 12, 45),
            status="Cours annulé",
            subject=MockSubject("HISTOIRE-GÉOGRAPHIE"),
            teacher_names=["YAKHLEF R."],
            canceled=True,
        ),
        Mock(
            background_color="#FF0080",
            classrooms=["06"],
            end=datetime(2022, 5, 25, 14, 35),
            group_names=[],
            start=datetime(2022, 5, 25, 13, 40),
            status="Cours annulé",
            subject=MockSubject("ANGLAIS"),
            teacher_names=["HAFIDI M."],
            canceled=True,
        ),
        Mock(
            background_color="#EC6719",
            classrooms=[],
            end=datetime(2022, 5, 25, 15, 35),
            group_names=["[2 ALLD LVB]"],
            start=datetime(2022, 5, 25, 14, 40),
            status="Cours annulé",
            subject=MockSubject("ALLEMAND"),
            teacher_names=["SAKR S."],
            canceled=True,
        )
    ]


@pytest.fixture(scope="module")
def friday_schedule() -> list[Mock]:
    """Returns an example of a schedule."""
    # 2022-04-20
    return [
        Mock(
            background_color="#FF0080",
            classrooms=["07"],
            end=datetime(2022, 4, 20, 9, 40),
            group_names=[],
            start=datetime(2022, 4, 20, 8, 45),
            status="Cours déplacé",
            subject=MockSubject("ANGLAIS"),
            teacher_names=["HAFIDI M."],
            canceled=False,
        ),
        Mock(
            background_color="#800000",
            classrooms=["211 - Info"],
            end=datetime(2022, 4, 20, 14, 35),
            group_names=[],
            start=datetime(2022, 4, 20, 13, 40),
            status="Prof. absent",
            subject=MockSubject("ACC PERSO"),
            teacher_names=["BELHADJ N."],
            canceled=True,
        ),
        Mock(
            background_color="#FF8080",
            classrooms=["05"],
            end=datetime(2022, 4, 20, 13, 40),
            group_names=[],
            start=datetime(2022, 4, 20, 12, 45),
            status=None,
            subject=MockSubject("SC. ECO & SOC."),
            teacher_names=["BEN OTHMAN N."],
            canceled=False,
        ),
        Mock(
            background_color="#FFFF00",
            classrooms=["07"],
            end=datetime(2022, 4, 20, 9, 40),
            group_names=[],
            start=datetime(2022, 4, 20, 7, 45),
            status="Prof. absent",
            subject=MockSubject("MATHÉMATIQUES"),
            teacher_names=["BELHADJ N."],
            canceled=True,
        ),
        Mock(
            background_color="#0080FF",
            classrooms=["06"],
            end=datetime(2022, 4, 20, 11, 50),
            group_names=[],
            start=datetime(2022, 4, 20, 10, 55),
            status="Cours déplacé",
            subject=MockSubject("FRANÇAIS"),
            teacher_names=["DJERAD K."],
            canceled=False,
        ),
        Mock(
            background_color="#0080FF",
            classrooms=["06"],
            end=datetime(2022, 4, 20, 15, 35),
            group_names=[],
            start=datetime(2022, 4, 20, 14, 40),
            status=None,
            subject=MockSubject("FRANÇAIS"),
            teacher_names=["DJERAD K."],
            canceled=False,
        ),
        Mock(
            background_color="#FF0080",
            classrooms=["07"],
            end=datetime(2022, 4, 20, 10, 50),
            group_names=[],
            start=datetime(2022, 4, 20, 9, 55),
            status=None,
            subject=MockSubject("ANGLAIS"),
            teacher_names=["HAFIDI M."],
            canceled=False,
        )
    ]
