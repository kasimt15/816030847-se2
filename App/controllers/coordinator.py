from sqlalchemy.exc import IntegrityError
from App.models import Coordinator
from App.database import db

def create_coordinator(name, address):
    try:
        new_coordinator = Coordinator(name=name, address=address)
        db.session.add(new_coordinator)
        db.session.commit()
        return f"Coordinator '{name}' created successfully."

    except IntegrityError as e:
        db.session.rollback()

        if "UNIQUE constraint failed" in str(e):
            return f"A coordinator with the name '{name}' already exists."
        else:
            return f"An error occurred while creating the coordinator: {str(e)}"
    
    except Exception as e:
        db.session.rollback()
        return f"An unexpected error occurred: {str(e)}"

def get_coordinator_by_name(name):
    comp= coordinator.query.filter_by(name=name).first()
    return comp

def get_coordinatorid(id):
    return Coordinator.query.get(id)

def get_coordinator_by_venue(venue):
    return coordinator.query.filter_by(venue).first()

def get_all_coordinator():
    return coordinator.query.all()

def get_all_coodinators_json():
    coordinators = Coordinator.query.all()
    if not coordinators:
        return []
    coordinators = [coordinator.get_json() for coordinator in coordinators]
    return coordinators