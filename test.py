import unittest
import json
from app import create_app
from app.models import db, Pokemon, User
import base64


app = create_app("test")


class PokemonTest(unittest.TestCase):

    def setUp(self):
        app.app_context().push()
        db.create_all()
        pokemon1 = Pokemon(id=3, name='Venusaur', type1='Grass', type2='Poison', total=525, hp=80,
                           attack=82, defense=83, sp_attack=100, sp_defense=100, speed=80, generation=1, legendary=False)
        pokemon2 = Pokemon(id=344, name='Claydol', type1='Ground', type2='Psychic', total=500, hp=60,
                           attack=70, defense=105, sp_attack=70, sp_defense=120, speed=75, generation=3, legendary=False)
        pokemon3 = Pokemon(id=380, name='LatiasMega Latias', type1='Dragon', type2='Psychic', total=700, hp=80,
                           attack=100, defense=120, sp_attack=140, sp_defense=110, speed=75, generation=3, legendary=True)

        user1 = User(username="test-user")
        user1.hash_password("1234")
        db.session.add(pokemon1)
        db.session.add(pokemon2)
        db.session.add(pokemon3)
        db.session.add(user1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_register(self):
        client = app.test_client(self)
        response = client.post('/user/register', data=json.dumps(
            {"username": "test", "password": "1234"}), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"username": "test"})

    def test_pokemon_without_user(self):
        client = app.test_client(self)
        response = client.get('/pokemon')
        self.assertEqual(response.status_code, 401)

    def test_pokemon_with_user(self):
        client = app.test_client(self)
        response = client.get('/pokemon', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(response.status_code, 200)

    def test_pokemon_filter_name(self):
        client = app.test_client(self)
        response = client.get('/pokemon?name=s', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(len(response.json['pokemons']), 2)
        self.assertEqual(response.json['pokemons'][0]['name'], "Venusaur")
        self.assertEqual(response.json['pokemons']
                         [1]['name'], "LatiasMega Latias")

    def test_pokemon_filter_type1(self):
        client = app.test_client(self)
        response = client.get('/pokemon?type1=Grass', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(response.json['pokemons'][0]['id'], 3)

    def test_pokemon_filter_type2(self):
        client = app.test_client(self)
        response = client.get('/pokemon?type2=Psychic', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(len(response.json['pokemons']), 2)
        self.assertEqual(response.json['pokemons'][0]['id'], 344)
        self.assertEqual(response.json['pokemons'][1]['id'], 380)

    def test_pokemon_sort(self):
        client = app.test_client(self)
        response = client.get('/pokemon?sort=-hp,name', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(response.json['pokemons'][0]['id'], 380)
        self.assertEqual(response.json['pokemons'][1]['id'], 3)
        self.assertEqual(response.json['pokemons'][2]['id'], 344)

    def test_pokemon_attack(self):
        client = app.test_client(self)
        response = client.get('/pokemon?attack={"lt": 110, "gte": 80}&sort=-total', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(len(response.json['pokemons']), 2)
        self.assertEqual(response.json['pokemons'][0]['id'], 3)
        self.assertEqual(response.json['pokemons'][1]['id'], 380)

    def test_pokemon_legendary(self):
        client = app.test_client(self)
        response = client.get('/pokemon?legendary=1', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(len(response.json['pokemons']), 1)

    def test_pokemon_defense(self):
        client = app.test_client(self)
        response = client.get('/pokemon?defense={"lte": 110}', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(response.json['pokemons'][0]['id'], 3)

    def test_pokemon_generation(self):
        client = app.test_client(self)
        response = client.get('/pokemon?generation={"eq": 3}&sort=sp_defense', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(len(response.json['pokemons']), 2)
        self.assertEqual(response.json['pokemons'][0]['id'], 380)
        self.assertEqual(response.json['pokemons'][1]['id'], 344)

    def test_pokemon_hp_speed(self):
        client = app.test_client(self)
        response = client.get('/pokemon?hp={"gte": 80}&type1=Dragon', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(len(response.json['pokemons']), 1)
        self.assertEqual(response.json['pokemons'][0]['id'], 380)

    def test_pokemon_name_type2_sp_attack(self):
        client = app.test_client(self)
        response = client.get('/pokemon?name=l&type2=Psychic&sp_attack={"gte": 60, "lt": 80}', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(len(response.json['pokemons']), 1)
        self.assertEqual(response.json['pokemons'][0]['id'], 344)

    def test_user_register_without_json(self):
        client = app.test_client(self)
        response = client.post(
            '/user/register', headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_user_register_with_json_without_password(self):
        client = app.test_client(self)
        response = client.post('/user/register', data=json.dumps(
            {"username": "usera12"}), headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_pokemon_numeric_fields_invalid_json(self):
        client = app.test_client(self)
        response = client.get('/pokemon?name=l&type2=Psychic&sp_attack=10', headers={"Authorization": "Basic {}".format(
            base64.b64encode(b"test-user:1234").decode("utf8"))})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
