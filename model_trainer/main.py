import pandas as pd
# Configurações para exibir todo o DataFrame sem truncamento
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
from data_loader import DataLoader
from preprocessor import Preprocessor
from persistence import save_semantic_layer
from eda import ExploratoryDataAnalyzer
from pycaret_trainer import PyCaretTrainer
from model import ModelTrainer
from model import plot_feature_importance

def main():
    # Etapa 1 – Carregar dados
    loader = DataLoader()
    df = loader.load_soya_features()

    preprocessor = Preprocessor(df)
    preprocessor.clean()
    preprocessor.fill_missing_values()
    preprocessor.complete_paraguay_china()
    preprocessor.filter_by_area()
    
    # Etapa 2 – Análise Exploratória de Dados (EDA)
    # eda = ExploratoryDataAnalyzer(df)
    # eda.run()

    # Etapa 3 – Treinamento com PyCaret
    # pycaret_trainer = PyCaretTrainer(df, target='production')
    # pycaret_trainer.run()

    # Etapa 4 – Treinar
    X_train, X_test, y_train, y_test = preprocessor.get_features_and_target()
    trainer = ModelTrainer(X_train, X_test, y_train, y_test)
    trainer.train()
    trainer.evaluate()

    future_df = preprocessor.forecast_features_next_year(window = 9)
    feature_cols = X_train.columns
    X_future = future_df[feature_cols]

    # 2. Aplica o modelo para prever produção
    future_df["production"] = trainer.predict(X_future)
    future_df["tipo_dado"] = "projetado"

    # 4. Prepara os dados já ocorridos
    historico_df = preprocessor.df.copy()
    historico_df["tipo_dado"] = "real"

    # 5. Concatena os dois conjuntos
    df_final = pd.concat([historico_df, future_df], ignore_index=True)
    df_final = df_final.sort_values(by=["area", "year"]).reset_index(drop=True)
    # 6. Salva a camada semântica completa
    save_semantic_layer(df_final)
    # plot_feature_importance(trainer.model, X_train.columns)
    # trainer.save()

if __name__ == "__main__":
    main()
