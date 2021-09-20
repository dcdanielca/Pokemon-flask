from app.models import User, Pokemon
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

TEXT_FIELDS = {
    'name': Pokemon.name.ilike
}

CATEGORY_FIELDS = {
    'type1': Pokemon.type1,
    'type2': Pokemon.type2,
    'legendary': Pokemon.legendary
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


def search_numeric(column, operators, query):
    filter_list = []
    if "eq" in operators:
        filter_list.append(column == operators['eq'])
    if "lt" in operators:
        filter_list.append(column < operators['lt'])
    if "lte" in operators:
        filter_list.append(column <= operators['lte'])
    if "gt" in operators:
        filter_list.append(column > operators['gt'])
    if "gte" in operators:
        filter_list.append(column >= operators['gte'])

    return query.filter(*filter_list)


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return True
