import psycopg2
import os
from processor.FAOSTATLoader import FAOSTATLoader
from processor.DatasetBuilder import DatasetBuilder

def salvar_features(df):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "faostat"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS features_soja (
            id SERIAL PRIMARY KEY,
            area VARCHAR(100),
            year INT,
            production NUMERIC,
            use_per_capita NUMERIC,
            use_per_area_of_cropland NUMERIC,
            agricultural_use NUMERIC,
            temperature_change NUMERIC,
            investment_usd NUMERIC,
            rural_population NUMERIC,
            producer_price NUMERIC,
            data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO features_soja (
                area, year, area_harvested, production, yield,
                agricultural_use, use_per_area_of_cropland, use_per_capita,
                temperature_change, investment_usd, rural_population, producer_price
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
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

    print("✅ Features carregadas:")
    print(df_final.head())
    salvar_features(df_final)

if __name__ == "__main__":
    main()
