import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv 

load_dotenv()

class DataLoader:
    def __init__(self):
        host = os.getenv("POSTGRES_HOST")
        db = os.getenv("POSTGRES_DB")
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        port = os.getenv("POSTGRES_PORT")
        self.conn_str = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        self.engine = create_engine(self.conn_str)

    def load_soya_features(self) -> pd.DataFrame:
        """ Carrega os dados da tabela soya_features do PostgreSQL.
        Retorna um DataFrame do pandas.
        """
        df = pd.read_sql("SELECT * FROM soya_features", self.engine)
        return df
