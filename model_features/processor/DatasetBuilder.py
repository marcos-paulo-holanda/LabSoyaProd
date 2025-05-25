
class DatasetBuilder:
    """
    Classe responsável por carregar e unificar os dataframes de diferentes fontes.
    """
    def __init__(self, loader):
        self.loader = loader
        self.df_final = None

    def carregar_dados(self):
        print("🔄 Carregando todos os dataframes...")
        self.df_soya = self.loader.load_dataframe('qcl')
        self.df_fert = self.loader.load_dataframe('rfn')
        self.df_temp = self.loader.load_dataframe('et')
        self.df_inv = self.loader.load_dataframe('ic').rename(columns={"Value US$": "Investment_USD"})
        self.df_pop = self.loader.load_dataframe('oa')
        self.df_price = self.loader.load_dataframe('pp')

    def merge_dados(self):
        print("🔗 Unificando os dataframes...")
        df = self.df_soya.merge(self.df_fert, on=["Area", "Year"], how="outer")
        df = df.merge(self.df_temp, on=["Area", "Year"], how="outer")
        df = df.merge(self.df_inv, on=["Area", "Year"], how="outer")
        df = df.merge(self.df_pop, on=["Area", "Year"], how="outer")
        df = df.merge(self.df_price, on=["Area", "Year"], how="outer")
        self.df_final = df

    def executar(self):
        self.carregar_dados()
        self.merge_dados()
        return self.df_final