from models import db
from sqlalchemy import create_engine
from app import app
import pandas as pd

sql_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
connection = sql_engine.raw_connection()

if __name__ == "__main__":
    column_names =  ["id", "name", "type1", "type2", "total", "hp", "attack", "defense", "sp_attack", "sp_defense", "speed", "generation", "legendary"]
    
    with open('pokemon.csv') as csv_file:
        df = pd.read_csv(csv_file, header = 0, names = column_names, index_col ="id")
        df.to_sql('pokemon', con=connection, if_exists='replace')