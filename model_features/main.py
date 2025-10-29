import os, psycopg2
from processor.FAOSTATLoader import FAOSTATLoader
from processor.DatasetBuilder import DatasetBuilder
from queries import *
from dotenv import load_dotenv

load_dotenv()
"""
Script para construir e salvar as features de soja no banco de dados PostgreSQL.
Conecta-se à camada bronze, processa os dados e salva as features em uma tabela específica (camada prata).
"""
def save_features(df):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute(SOYA_FEATURES_TABLE)

    for _, row in df.iterrows():
        cursor.execute(INSERT_SOYA_FEATURES, (
        row.get("Area"),
        row.get("Year"),
        row.get("Area harvested"),
        row.get("Production"),
        row.get("Yield"),
        row.get("Agricultural Use"),
        row.get("Use per area of cropland"),
        row.get("Use per capita"),
        row.get("Temperature change"),
        row.get("Investment_USD"),
        row.get("Rural population"),
        row.get("Producer Price (USD/tonne)")
    ))

    conn.commit()
    cursor.close()
    conn.close()

def main():
    loader = FAOSTATLoader()
    builder = DatasetBuilder(loader)
    df_final = builder.executar()
    save_features(df_final)

if __name__ == "__main__":
    main()
