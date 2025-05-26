-- Cria a tabela features_soja que armazena os dados de produção de soja de vários países
-- e suas respectivas características, como área cultivada, ano, produção, uso per capita,
-- uso por área de terras cultivadas, uso agrícola, mudança de temperatura, investimento em
-- dólares, população rural e preço do produtor. 
DROP TABLE IF EXISTS features_soja;

CREATE TABLE IF NOT EXISTS features_soja (
    id SERIAL PRIMARY KEY,
    area CHARACTER VARYING,
    year CHARACTER VARYING,
    area_harvested CHARACTER VARYING,
    production CHARACTER VARYING,
    yield CHARACTER VARYING,
    agricultural_use CHARACTER VARYING,
    use_per_area_of_cropland CHARACTER VARYING,
    use_per_capita CHARACTER VARYING,
    temperature_change CHARACTER VARYING,
    investment_usd CHARACTER VARYING,
    rural_population CHARACTER VARYING,
    producer_price CHARACTER VARYING,
    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


