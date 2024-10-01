from App.database import db

class Coordinated(db.Model):
    __tablename__ = 'coordinated'

    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'), primary_key=True)
    coordinator_id = db.Column(db.Integer, db.ForeignKey('coordinator.id'), primary_key=True)

    competition = db.relationship('Competition', back_populates='coordinated')
    coordinator = db.relationship('Coordinator', back_populates='coordinated')

    def __init__(self, competition_id, coordinator_id):
        self.competition_id = competition_id
        self.coordinator_id = coordinator_id

    def get_json(self):
        return {
            'competition id': self.competition_id,
            'coordinator id': self.coordinator_id,
            'competition name': self.competition.name,
            'coordinator name': self.coordinator.name
        }
