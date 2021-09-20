from sqlalchemy import create_engine
from config import PATH_DB
import pandas as pd

engine = create_engine(f'sqlite:///{PATH_DB}', echo=False)

if __name__ == "__main__":
    column_names = ["id", "name", "type1", "type2", "total", "hp", "attack",
                    "defense", "sp_attack", "sp_defense", "speed", "generation", "legendary"]

    with open('pokemon.csv') as csv_file:
        df = pd.read_csv(csv_file, header=0, names=column_names)
        df.to_sql('pokemon', con=engine, if_exists='replace',  index=False)
