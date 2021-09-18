from models import Pokemon, User, db
from flask import jsonify, request, abort
from sqlalchemy import text
from extras import search_numeric, auth
from config import app, SORT_FIELDS, NUMERIC_FIELDS
import json


db.init_app(app)

@app.route("/pokemon")
@auth.login_required
def pokemon():
    params = request.args
    query = Pokemon.query

    if len(params) != 0:
        if 'name' in params:
            query = query.filter(Pokemon.name.ilike(f'%{params["name"]}%'))

        if 'type1' in params:
            query = query.filter(Pokemon.type1 == params['type1'])

        if 'type2' in params:
            query = query.filter(Pokemon.type2 == params['type2'])

        if 'hp' in params:
            operators = json.loads(params['hp'])
            query = search_numeric(NUMERIC_FIELDS['hp'], operators, query)

        if 'attack' in params:
            operators = json.loads(params['attack'])
            query = search_numeric(NUMERIC_FIELDS['attack'], operators, query)

        if 'defense' in params:
            operators = json.loads(params['defense'])
            query = search_numeric(NUMERIC_FIELDS['defense'], operators, query)

        if 'sp_attack' in params:
            operators = json.loads(params['sp_attack'])
            query = search_numeric(NUMERIC_FIELDS['sp_attack'], operators, query)

        if 'sp_defense' in params:
            operators = json.loads(params['sp_defense'])
            query = search_numeric(NUMERIC_FIELDS['sp_attack'], operators, query)

        if 'speed' in params:
            operators = json.loads(params['speed'])
            query = search_numeric(NUMERIC_FIELDS['speed'], operators, query)

        if 'generation' in params:
            operators = json.loads(params['generation'])
            query = search_numeric(NUMERIC_FIELDS['generation'], operators, query)

        if 'legendary' in params:
            query = query.filter(Pokemon.legendary == params['legendary'])

        if 'sort' in params:
            sort_text = ",".join(SORT_FIELDS.get(text) for text in params['sort'].split(',') if SORT_FIELDS.get(text) is not None)
            query = query.order_by(text(sort_text))


    return jsonify({"pokemons" : [pokemon.serialize for pokemon in query.limit(20)]})



@app.route('/user/register', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) 
    if User.query.filter_by(username = username).first() is not None:
        abort(400)
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201