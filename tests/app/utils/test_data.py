from unittest.mock import Mock

from app.utils.schedule import jsonify_schedule


def test_jsonify_schedule(
        wednesday_schedule: list[Mock],
        thursday_schedule: list[Mock],
        friday_schedule: list[Mock]
) -> None:
    """Test the jsonify_schedule function."""
    assert jsonify_schedule(wednesday_schedule) == [
        {
            "background_color": "#FFFF00",
            "classrooms": ["07"],
            "end": "09:40",
            "group_names": [],
            "start": "07:45",
            "status": None,
            "subject": "MATHÉMATIQUES",
            "teachers": ["BELHADJ N."]
        },
        {
            "background_color": "#FF0080",
            "classrooms": ["07"],
            "end": "10:50",
            "group_names": [],
            "start": "09:55",
            "status": None,
            "subject": "ANGLAIS",
            "teachers": ["HAFIDI M."]
        },
        {
            "background_color": "#0080FF",
            "classrooms": ["06"],
            "end": "11:50",
            "group_names": [],
            "start": "10:55",
            "status": "Cours déplacé",
            "subject": "FRANÇAIS",
            "teachers": ["DJERAD K."]
        },
        {
            "background_color": "#75B951",
            "classrooms": ["13"],
            "end": "12:45",
            "group_names": ["[2 SL G1]"],
            "start": "11:50",
            "status": None,
            "subject": "SCIENCES & LABO",
            "teachers": ["SAAB M."]
        },
        {
            "background_color": "#FF8080",
            "classrooms": ["05"],
            "end": "13:40",
            "group_names": [],
            "start": "12:45",
            "status": "Prof. absent",
            "subject": "SC. ECO & SOC.",
            "teachers": ["BEN OTHMAN N."]
        },
        {
            "background_color": "#800000",
            "classrooms": ["211 - Info"],
            "end": "14:35",
            "group_names": [],
            "start": "13:40",
            "status": "Changement de salle",
            "subject": "ACC PERSO",
            "teachers": ["BELHADJ N."]
        },
        {
            "background_color": "#0080FF",
            "classrooms": ["06"],
            "end": "15:35",
            "group_names": [],
            "start": "14:40",
            "status": "Cours annulé",
            "subject": "FRANÇAIS",
            "teachers": ["DJERAD K."]
        }
    ]

    assert jsonify_schedule(thursday_schedule) == [
        {
            "background_color": "#C0C0C0",
            "classrooms": [],
            "end": "15:35",
            "group_names": [],
            "start": "07:45",
            "status": "Exceptionnel",
            "subject": "ED.PHYSIQUE & SPORT.",
            "teachers": ["NEGHNAGH N.", "SAADOUNE S.", "CATRY V.", "DRIDI M."]
        }
    ]

    assert jsonify_schedule(friday_schedule) == [
        {
            "background_color": "#FF0080",
            "classrooms": ["07"],
            "end": "09:40",
            "group_names": [],
            "start": "08:45",
            "status": "Cours déplacé",
            "subject": "ANGLAIS",
            "teachers": ["HAFIDI M."]
        },
        {
            "background_color": "#FF0080",
            "classrooms": ["07"],
            "end": "10:50",
            "group_names": [],
            "start": "09:55",
            "status": None,
            "subject": "ANGLAIS",
            "teachers": ["HAFIDI M."]
        },
        {
            "background_color": "#0080FF",
            "classrooms": ["06"],
            "end": "11:50",
            "group_names": [],
            "start": "10:55",
            "status": "Cours déplacé",
            "subject": "FRANÇAIS",
            "teachers": ["DJERAD K."]
        },
        {
            "background_color": "#FF8080",
            "classrooms": ["05"],
            "end": "13:40",
            "group_names": [],
            "start": "12:45",
            "status": None,
            "subject": "SC. ECO & SOC.",
            "teachers": ["BEN OTHMAN N."]
        },
        {
            "background_color": "#800000",
            "classrooms": ["211 - Info"],
            "end": "14:35",
            "group_names": [],
            "start": "13:40",
            "status": "Prof. absent",
            "subject": "ACC PERSO",
            "teachers": ["BELHADJ N."]
        },
        {
            "background_color": "#0080FF",
            "classrooms": ["06"],
            "end": "15:35",
            "group_names": [],
            "start": "14:40",
            "status": None,
            "subject": "FRANÇAIS",
            "teachers": ["DJERAD K."]
        }
    ]
