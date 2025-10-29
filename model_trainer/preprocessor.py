import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split

class Preprocessor:
    """Classe para definir a camada abstrata de dados a serem consumidos pelo modelo de Machine Learning.
    Esta classe é responsável por limpar, filtrar e preparar os dados para o treinamento do modelo"""
    def __init__(self, df):
        self.df = df

    def clean(self) -> pd.DataFrame:
        """Limpa o DataFrame removendo linhas com valores ausentes e convertendo tipos de dados.
        Retorna um DataFrame limpo.
        """
        df = self.df.copy()
        df = df[df['year'].astype(int) <= datetime.now().year]
        df.replace(["NaN", "None", ""], np.nan, inplace=True)

        for col in df.columns:
            if col not in ['area', 'year', 'data_execucao']:
                df[col] = df[col].astype(float)

        self.df = df
    
    def filter_by_area(self) -> pd.DataFrame:
        """Filtra o DataFrame por uma área específica.
        Retorna um DataFrame filtrado.
        """
        df = self.df.copy()
        principais_paises = [
            "Brazil", "United States of America", "Argentina",
            "India", "China", "Paraguay", "Canada"
        ]
        df = df[df['area'].isin(principais_paises)]
        self.df = df

    def fill_missing_values(self):
        id_cols = ["area", "year"]
        df = self.df.copy()
        df = df.sort_values(by=id_cols)
        value_cols = [col for col in df.columns if col not in id_cols]
        df[value_cols] = df.groupby("area")[value_cols].transform(lambda group: group.ffill().bfill())
        self.df = df

    def get_features_and_target(self):
        X = self.df.drop(columns=['production', 'area', 'year', 'data_execucao'])
        y = self.df['production']
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def complete_paraguay_china(self):
        """Preenche os valores ausentes de 'investment_usd' para o Paraguai com base na média anual
        dos países vizinhos (Argentina, Brazil, Bolivia), e os valores ausentes de 'investment_usd' 
        e 'producer_price' para a China com base na média anual de países asiáticos semelhantes 
        (India, Vietnam, Indonesia)."""
        df = self.df.copy()

        # Vizinhos do Paraguai
        vizinhos_paraguai = ['Argentina', 'Brazil', 'Bolivia']
        media_paraguai_ano = df[df['area'].isin(vizinhos_paraguai)].groupby('year')['investment_usd'].mean()

        mask_paraguay = (df['area'] == 'Paraguay') & (df['investment_usd'].isna())
        df.loc[mask_paraguay, 'investment_usd'] = df.loc[mask_paraguay, 'year'].map(media_paraguai_ano)

        # Vizinhos da China
        vizinhos_china = ['India', 'Vietnam', 'Indonesia']
        df_vizinhos_china = df[df['area'].isin(vizinhos_china)]
        
        media_china_invest_ano = df_vizinhos_china.groupby('year')['investment_usd'].mean()
        media_china_price_ano = df_vizinhos_china.groupby('year')['producer_price'].mean()

        mask_china_invest = (df['area'] == 'China') & (df['investment_usd'].isna())
        mask_china_price = (df['area'] == 'China') & (df['producer_price'].isna())

        df.loc[mask_china_invest, 'investment_usd'] = df.loc[mask_china_invest, 'year'].map(media_china_invest_ano)
        df.loc[mask_china_price, 'producer_price'] = df.loc[mask_china_price, 'year'].map(media_china_price_ano)

        self.df = df

    def forecast_features_next_year(self, window: int = 9) -> pd.DataFrame:
        """
        Cria um DataFrame com as features projetadas para o ano posterior ao último,
        usando a variação média dos últimos `window` anos de cada país.
        """
        df = self.df.copy()
        last_year = int(df["year"].max())
        next_year = last_year + 1

        # Quais colunas são numéricas e entram no modelo?
        numeric_cols = [c for c in df.columns
                        if c not in ["area", "year", "data_execucao", "production"]]

        forecasts = []
        for area, group in df.groupby("area"):
            group = group.sort_values("year")
            recent = group.tail(window + 1)          # últimos N+1 anos
            last_vals = recent.iloc[-1][numeric_cols]

            # variação ano-a-ano média
            deltas = recent[numeric_cols].diff().tail(window).mean()

            # previsão = último valor + média da variação
            predicted_vals = last_vals + deltas.fillna(0)  # fallback se algum delta for NaN

            row = {"area": area, "year": next_year}
            row.update(predicted_vals.to_dict())
            forecasts.append(row)

        forecast_df = pd.DataFrame(forecasts)

        # Se o modelo espera exatamente o mesmo conjunto de colunas,
        # garanta a mesma ordem:
        return forecast_df[["area", "year"] + numeric_cols]


