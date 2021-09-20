# Installation

The API was developed using Python 3.9. I recommend using this version to avoid any inconvenience.

## How to install

1. Install Python 3.9 (recommended) in your PC.
2. Install virtualenv with Python 3.9
2. Clone the repository
3. Create virtualenv `python3.9 -m virtualenv venv`
4. Active the venv `source venv/bin/activate`
5. Install the requirements `pip install -r requirements.txt`

## Initial Configuration

Before installing, importing database and running, you need to configure some parameters for the database.

1. Open the file `config_test.py` and `config.py`.
2. Change the code line `PATH_DB` with the corresponding path where you want to create the databases for test and dev respectively.
3. Also in these files you can modify other parameters if you consider it necessary, like for example the port
3. Save the changes

## Creating database

To create the database with corresponding tables:

1. From the console in the root path of the project and with virtualenv active run `python`
2. In the python console execute `from app import create_app`
3. In the python console execute `from app.models import db`
4. Finally, execute `db.create_all(app=create_app())`

## Importing pokemon.csv

To import database of pokemons run `python import.py`

# Unit Test

The API has 16 unit tests, to verify that everything is correct. Run `python test.py`

# Usage

If you use Postman, In the file `Pokemon.postman_collection.json` is the collection to import.
The api has 2 endpoints:

## Register User

This endpoint allows you to create a user to be able to authenticate with it later to the API. 

Endpoint: `/user/register`

Method: `POST`

Body (JSON): `{"username:" "myuser", "password": "mypass"}`


##  Get Pokemon

This endpoint allow you to get pokemons, according to various url query parameters:

- Text fields are parameters that allow you to search for a string in one of the fields. The only parameter that allows this is `name`. Example `?name=Pik`, allow search all pokemons that in its name contains `Pik`. This field is case insensitive.
- Category fields are parameter that allow you to search by value in field. The fields `type1` `type2` `legendary` allow do this. Example `type1=Water` `type2=Dragon` `legendary=0` (Legendary: 1 for True or  0 for False)
- Numeric fields are parameters that allow search value equal(eq), less than(lt), less than or equal(lte), greater than(gt), greater equal or than(gte). The fields `hp` `attack` `defense` `sp_attack` `sp_defense` `speed` `generation` allow do this. How it works?
    1. You write the query parameter with one field. For example `?speed=`
    2. The query parameter expect one JSON with the search. (eq, lt, lte, gt or gte) For example, you want pokemon with speed less than 100 and greater than 50 `?speed={"lt": 100, "gt": 50}`
    3. **Note:** you can use as many numerical fields as you want with as many operators as you want.
- Sort fields are parameters to order pokemons by one or more fields (**You can use any field except id**). How it works?
    - You write comma-separated fields and before each field write `"-"` if you want descending order. For example: You can order first by defense asc and name desc. So you write `?sort=defense,-name`

**Note**: You can use any combination of the above to filter. If you don't set any of the above, all pokemon will be brought in by default.
