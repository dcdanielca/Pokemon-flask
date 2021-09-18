from models import User
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


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
    user =  User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    return True