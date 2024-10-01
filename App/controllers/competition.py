from App.models import Competition
from App.database import db

def create_competition(name, venue, date, start_time, end_time, participant):
    new_competition= Competition(name= name, venue= venue, date= date, start_time= start_time, end_time= end_time, num_of_participants=participant)
    db.session.add(new_competition)
    db.session.commit()
    return

def get_competition_by_name(name):
    comp= Competition.query.filter_by(name=name).first()
    return comp

def get_competitionid(id):
    return Competition.query.get(id)

def get_competition_by_venue(venue):
    return Competition.query.filter_by(venue).first()

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    Competitions = Competition.query.all()
    if not Competitions:
        return []
    Competitions = [Competition.get_json() for Competition in Competitions]
    return Competitions