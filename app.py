from models import Pokemon
from config import *
from flask import jsonify

@app.route("/pokemon")
def pokemon():
    return jsonify({"pokemons" : [pokemon.serialize for pokemon in Pokemon.query.all()]})