from App.database import db

class Competition(db.Model):
    __tablename__ = 'competition'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    num_of_participants = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    coordinator_id = db.Column(db.Integer, db.ForeignKey("coordinator.id"))

    participations = db.relationship("Participation", back_populates="competition")
    coordinated = db.relationship('Coordinated', back_populates='competition')

    def __init__(self, name, venue, date, start_time, end_time, num_of_participants):
        self.name = name
        self.venue = venue
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.num_of_participants = num_of_participants

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'venue': self.venue,
            'date': self.date,
            'start time': self.start_time,
            'end time': self.end_time,
            'number of participants': self.num_of_participants
        }
