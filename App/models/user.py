from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(20), nullable=False, unique=True)
    address= db.Column(db.String(100), nullable= False)

    participations= db.relationship("Participation", back_populates="student")

    def __init__(self, name, address):
        self.name = name
        self.address= address

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'participations': [participation.get_json() for participation in self.participations]
        }

