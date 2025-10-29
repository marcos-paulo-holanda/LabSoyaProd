SOYA_FEATURES_TABLE = """
        CREATE TABLE IF NOT EXISTS soya_features (
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
    """

INSERT_SOYA_FEATURES = """
            INSERT INTO soya_features (
                area, year, area_harvested, production, yield,
                agricultural_use, use_per_area_of_cropland, use_per_capita,
                temperature_change, investment_usd, rural_population, producer_price
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """