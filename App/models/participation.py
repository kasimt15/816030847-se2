from App.database import db

class Participation(db.Model):
    competition_id= db.Column(db.Integer, db.ForeignKey("competition.id"), primary_key= True, nullable=False)
    student_id= db.Column(db.Integer, db.ForeignKey("user.id"), primary_key= True, nullable=False)

    student = db.relationship("User", back_populates="participations")
    competition = db.relationship("Competition", back_populates="participations")

    def __init__(self, student_id, competition_id):
        self.competition_id= competition_id
        self.student_id= student_id

    def get_json(self):
        return {
            'competition_id': self.competition_id,
            'student_id': self.student_id,
            'competition': self.competition.name,
            'student': self.student.name
        }