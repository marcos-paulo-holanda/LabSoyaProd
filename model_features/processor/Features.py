from processor.BaseProcessor import FAODataProcessor
from datetime import datetime

class SoyaProcessor(FAODataProcessor):
    """Classe para processar dados de produção de soja."""
    def filtrar_df(self, df):
        df = df[df['Item'] == 'Soya beans']
        return df

class FertilizersProcessor(FAODataProcessor):
    """Classe para processar dados de fertilizantes."""
    def filtrar_df(self, df):
        filtros = [
            'Agricultural Use',
            'Use per area of cropland',
            'Use per capita'
        ]
        df = df[df['Element'].isin(filtros)]
        return df

class ETProcessor(FAODataProcessor):
    """Classe para processar dados de temperatura."""
    def filtrar_df(self, df):
        # Filtra os dados para incluir apenas os elementos de temperatura
        df = df[df['Element'] == 'Temperature change']
        return df

    def executar(self):
        super().executar(aggfunc='mean')

class ICProcessor(FAODataProcessor):
    """Classe para processar dados de investimento e crédito na agricultura."""
    def filtrar_df(self, df):
        # Filtra os dados para incluir apenas os elementos de temperatura
        df = df[df['Element'] == 'Value US$']
        df = df[df['Item'] == 'Credit to Agriculture']
        return df

class OAPopulationProcessor(FAODataProcessor):
    """Classe para processar dados de população."""
    def filtrar_df(self, df):
        # Filtra os dados para incluir apenas os elementos de população rural
        df = df[df['Element'] == 'Rural population']
        return df

class PricesProcessor(FAODataProcessor):
    """Classe para processar dados de preços."""
    def filtrar_df(self, df):
        # Filtra os dados para incluir apenas os preços de soja
        df = df[df['Element'] == 'Producer Price (USD/tonne)']
        df = df[df['Item'] == 'Soya beans']
        return df