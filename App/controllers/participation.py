from sqlalchemy.exc import IntegrityError
from App.models import Participation
from App.database import db

def create_participation(student_id, competition_id):
    from App.controllers import get_competitionid
    try:
        new_participation= Participation(student_id= student_id, competition_id= competition_id)
        competition = get_competitionid(competition_id)
        
        if competition:
            competition.num_of_participants += 1
            db.session.add(new_participation)
            db.session.commit()
            return f"Participation created for student id {student_id} in competition id {competition_id}."
        else:
            return f"Competition with id {competition_id} not found."

    except IntegrityError as e:
        db.session.rollback()
        if "UNIQUE constraint failed" in str(e):
            return f"Participation already exists for student id {student_id} in competition id {competition_id}."
        else:
            return f"An error occurred: {str(e)}"

    except Exception as e:
        db.session.rollback()
        return f"An unexpected error occurred: {str(e)}"


def get_all_participations():
    return Participation.query.all()

def get_all_participants_json():
    Participations = Participation.query.all()
    if not Participations:
        return []
    Participations = [Participation.get_json() for Participation in Participations]
    return Participations