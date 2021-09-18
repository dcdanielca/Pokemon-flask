
from flask import Flask
from models import Pokemon, db


directory_db = '/tmp/pokemon.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{directory_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JSON_SORT_KEYS"] = False
app.config['SECRET_KEY'] = 'z?^Bn&Lp8qqX)FC3'


def create_app():
    db.init_app(app)
    return app


SORT_FIELDS = {
    'name': 'name asc',
    '-name': 'name desc',
    'type1': 'type1 asc',
    '-type1': 'type1 desc',
    'type2': 'type2 asc',
    '-type2': 'type2 desc',
    'hp': 'hp asc',
    '-hp': 'hp desc',
    'attack': 'attack asc',
    '-attack': 'attack desc',
    'defense': 'defense asc',
    '-defense': 'defense desc',
    'sp_attack': 'sp_attack asc',
    '-sp_attack': 'sp_attack desc',
    'sp_defense': 'sp_defense asc',
    '-sp_defense': 'sp_defense desc',
    'speed': 'speed asc',
    '-speed': 'speed desc',
    'generation': 'generation asc',
    '-generation': 'generation desc',
    'legendary': 'legendary asc',
    '-legendary': 'legendary desc',
}

NUMERIC_FIELDS = {
    'hp': Pokemon.hp,
    'attack': Pokemon.attack,
    'defense': Pokemon.defense,
    'sp_attack': Pokemon.sp_attack,
    'sp_defense': Pokemon.sp_defense,
    'speed': Pokemon.speed,
    'generation': Pokemon.generation,
}