from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

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

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
            'id': self.id,
            'name': self.name,
            'type1': self.type1,
            'type2': self. type2,
            'total': self.total,
            'hp': self.hp,
            'attack': self.attack,
            'defense': self.defense,
            'sp_attack': self.sp_attack,
            'sp_defense': self.sp_defense,
            'speed': self.speed,
            'generation': self.generation,
            'legendary': self.legendary
       }