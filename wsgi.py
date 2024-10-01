from datetime import datetime
import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.models import Competition
from App.models import Participation
from App.models import Coordinator, Coordinated
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize)
from App.controllers import (get_competition_by_name ,get_competition_by_venue, get_competitionid, create_competition, get_all_competitions, get_all_competitions_json)
from App.controllers import (create_participation, get_all_participations, get_all_participants_json)
from App.controllers import (create_coordinated, create_coordinator, get_all_coordinator, get_all_coodinators_json, get_all_coordinated_json)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("name", default="rob")
@click.argument("address", default="1440_johnson&johnson_st_hidden_leaf_village")
def create_user_command(name, address):
    new_user= create_user(name, address)

    if isinstance(new_user, User):
        print(f'{name} created!')
    else:
        print(new_user)

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
@user_cli.command("delete", help="Deletes users from database")
@click.argument("name", default="bob")
def delete_user_command(name):
    bob= User.query.filter_by(name= name).first()
    if not name:
        print(f'{name} was not found')
        return
    db.session.delete(bob)
    db.session.commit()
    print(f"{name} was deleted!!")
'''

competition_cli= AppGroup("competition", help="competition objects commands")
app.cli.add_command(competition_cli)

@competition_cli.command("create", help= "create a competition")
@click.argument("name", default= "code4runners")
@click.argument("venue", default= "online")
@click.argument("date", default= "2024-09-27")
@click.argument("start_time", default= "09:00:00")
@click.argument("end_time", default= "13:00:00")
@click.argument("participant", default= 0)
def create_competition_command(name, venue, date, start_time, end_time, participant):
    startTime= datetime.strptime(start_time, "%H:%M:%S").time()
    endTime= datetime.strptime(end_time, "%H:%M:%S").time()
    
    create_competition(name, venue, date, startTime, endTime, participant)
    print(f"{name} was created!")

@competition_cli.command("list", help="Lists competitions in the database")
@click.argument("format", default="string")
def list_competition_command(format):
    if format == 'string':
        print(get_all_competitions())
    else:
        print(get_all_competitions_json())

'''
@competition_cli.command("delete", help= "Delete competitions in the database")
@click.argument("name", default= "code4runners")
def delete_competition_command(name):
    compe= Competition.query.filter_by(name=name).first()
    if not compe:
        print(f"{name} was not found!")
        return
    db.session.delete(compe)
    db.session.commit()
    print(f"{name} was deleted!!")
'''


participant_cli = AppGroup("participation", help= "participantion objects commands")
app.cli.add_command(participant_cli)

@participant_cli.command("create", help="create a competition relationship")
@click.argument("student_id", default=1)
@click.argument("competition_id", default=1)
def create_participation_command(student_id, competition_id):
    text= create_participation(student_id, competition_id)
    print(text)

@participant_cli.command("list", help="Lists partitions in the database")
@click.argument("format", default="string")
def list_participation_command(format):
    if format == 'string':
        print(get_all_participations())
    else:
        print(get_all_participants_json())

@participant_cli.command("delete", help="Deletes participations in the database")
@click.argument("student_id", default=1)
@click.argument("competition_id", default=1)
def delete_partition_command(student_id, competition_id):
    participant = Participation.query.filter_by(student_id=student_id, competition_id=competition_id).first()
    if participant:
        db.session.delete(participant)
        db.session.commit()
        print(f"student id: {participant.student_id} and competition id: {participant.competition_id} were deleted!")
    else:
        print(f"no records containing student id: {student_id} and competition id: {competition_id}")


coordination_cli = AppGroup("coordination", help= "coordinated objects commands")
app.cli.add_command(coordination_cli)

@coordination_cli.command("create_user", help="Creates a coordinator")
@click.argument("name", default="micheal")
@click.argument("address", default="the void")
def create_coordinator_command(name, address):
    new_user= create_coordinator(name, address)

    if isinstance(new_user, Coordinator):
        print(f'{name} created!')
    else:
        print(new_user)

@coordination_cli.command("list_users", help="Lists users in the database")
@click.argument("format", default="string")
def list_coordinators_command(format):
    if format == 'string':
        print(get_all_coordinator())
    else:
        print(get_all_coodinators_json())


@coordination_cli.command("create", help="create a coordination relationship")
@click.argument("competition_id", default=1)
@click.argument("coordinator_id", default=1)
def create_coordination_command(competition_id, coordinator_id):
    text= create_coordinated(competition_id, coordinator_id)
    print(text)

@coordination_cli.command("list", help="Lists coordinations in the database")
@click.argument("format", default="string")
def list_coordination_command(format):
    if format == 'string':
        print(get_all_coordinated())
    else:
        print(get_all_coordinated_json())


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)