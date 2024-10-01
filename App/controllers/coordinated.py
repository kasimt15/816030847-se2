from sqlalchemy.exc import IntegrityError
from App.models import Coordinated
from App.database import db

def create_coordinated(coordinator_id, competition_id):
    from App.controllers import get_competitionid, get_coordinatorid
    
    try:
        new_coordinated = Coordinated(coordinator_id=coordinator_id, competition_id=competition_id)

        competition = get_competitionid(competition_id)
        coordinator = get_coordinatorid(coordinator_id)

        if competition and coordinator:
            db.session.add(new_coordinated)
            db.session.commit()
            return f"Coordinator id {coordinator_id} successfully assigned to competition id {competition_id}."
        else:
            return f"Either competition with id {competition_id} or coordinator with id {coordinator_id} not found."

    except IntegrityError as e:
        db.session.rollback()
        if "UNIQUE constraint failed" in str(e):
            return f"Coordinator id {coordinator_id} is already assigned to competition id {competition_id}."
        else:
            return f"An error occurred: {str(e)}"

    except Exception as e:
        db.session.rollback()
        return f"An unexpected error occurred: {str(e)}"

def get_all_coordinated():
    return Coordinated.query.all()

def get_all_coordinated_json():
    coordinated_entries = Coordinated.query.all()
    if not coordinated_entries:
        return []
    coordinated_json = [coordination.get_json() for coordination in coordinated_entries]
    return coordinated_json
