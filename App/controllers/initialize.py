from datetime import datetime
from .user import *
from .competition import *
from .participation import *
from .coordinated import *
from .coordinator import *
from App.controllers import user as user_controller
from App.controllers import competition as competition_controller
from App.controllers import coordinated as coordinated_controller
from App.controllers import coordinator as coordinator_controller

from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', '1234_imaginery_lane_hidden_sand_village')

    #create a competition
    start_time= "09:00:00"
    end_time= "13:00:00"
    startTime= datetime.strptime(start_time, "%H:%M:%S").time()
    endTime= datetime.strptime(end_time, "%H:%M:%S").time()

    create_competition("code4runners", "online", "2024-09-28", startTime, endTime, 0)

    #create a partition
    create_participation(user_controller.get_user(1).id, competition_controller.get_competitionid(1).id)

    #create a coordinatior
    create_coordinator("jane", "homeless")

    #create a coordination
    create_coordinated(coordinator_controller.get_coordinatorid(1).id, competition_controller.get_competitionid(1).id)

    
