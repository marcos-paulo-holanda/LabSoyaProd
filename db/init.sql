-- Cria a tabela features_soja que armazena os dados de produção de soja de vários países
-- e suas respectivas características, como área cultivada, ano, produção, uso per capita,
-- uso por área de terras cultivadas, uso agrícola, mudança de temperatura, investimento em
-- dólares, população rural e preço do produtor. 
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
