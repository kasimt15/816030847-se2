from App.database import db

class Coordinator(db.Model):
    __tablename__ = 'coordinator'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique= True)
    address = db.Column(db.String(100), nullable=False)

    coordinated = db.relationship('Coordinated', back_populates='coordinator')

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'coordinated': [Coordinated.get_json() for Coordinated in self.coordinated]
        }

