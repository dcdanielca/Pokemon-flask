from flask_sqlalchemy import SQLAlchemy
from app import app

directory_db = '/tmp/pokemon.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{directory_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    type1 = db.Column(db.String(20))
    type2 = db.Column(db.String(20))
    total = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    sp_attack = db.Column(db.Integer)
    sp_defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    generation = db.Column(db.Integer)
    legendary = db.Column(db.Boolean, default=False)
    


    def __repr__(self):
        return '<Pokemon %r>' % self.name