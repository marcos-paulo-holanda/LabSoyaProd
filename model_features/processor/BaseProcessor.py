import pandas as pd
import boto3
import io
from abc import ABC, abstractmethod

class FAODataProcessor(ABC):
    def __init__(self, minio_client, bucket, key):
        self.minio_client = minio_client
        self.bucket = bucket
        self.key = key
        self.df_raw = None
        self.df_filtered = None
        self.df_pivot = None

    def load_from_minio(self):
        print(f"📥 Lendo {self.key} do MinIO...")
        response = self.minio_client.get_object(Bucket=self.bucket, Key=self.key)
        self.df_raw = pd.read_parquet(io.BytesIO(response['Body'].read()))

    def tratar_valores(self):
        df = self.df_raw.copy()
        df = self.filtrar_df(df)
        df['Element'] = df['Element'].str.strip()
        df['Value'] = (
            df['Value']
            .astype(str)
            .str.replace('.', '', regex=False)
            .astype(float)/1000000
        )
        self.df_filtered = df

    @abstractmethod
    def filtrar_df(self, df):
        pass

    def pivotar(self, aggfunc='first'):
        self.df_pivot = self.df_filtered.pivot_table(
            index=['Area', 'Year'],
            columns='Element',
            values='Value',
            aggfunc=aggfunc
        ).reset_index()

    def executar(self, aggfunc='first'):
        self.load_from_minio()
        self.tratar_valores()
        self.pivotar(aggfunc=aggfunc)
