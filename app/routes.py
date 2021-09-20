from app.models import Pokemon, User, db
from flask import jsonify, request, abort
from sqlalchemy import text
from flask import current_app as app
from app.extras import search_numeric, auth, TEXT_FIELDS, CATEGORY_FIELDS, NUMERIC_FIELDS, SORT_FIELDS
import json


@app.route("/pokemon")
@auth.login_required
def pokemon():
    params = request.args
    query = Pokemon.query

    if len(params) != 0:
        for key in params.keys():
            if key in TEXT_FIELDS:
                query = query.filter(TEXT_FIELDS[key](f'%{params[key]}%'))
            elif key in CATEGORY_FIELDS:
                query = query.filter(CATEGORY_FIELDS[key] == params[key])
            elif key in NUMERIC_FIELDS:
                operators = json.loads(params[key])
                if type(operators) is not dict:
                    abort(400)
                query = search_numeric(NUMERIC_FIELDS[key], operators, query)
            elif key == 'sort':

                sort_text = ",".join(SORT_FIELDS.get(text) for text in params['sort'].split(
                    ',') if SORT_FIELDS.get(text) is not None)
                query = query.order_by(text(sort_text))
    return jsonify({"pokemons": [pokemon.serialize for pokemon in query.all()]})


@app.route('/user/register', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201
