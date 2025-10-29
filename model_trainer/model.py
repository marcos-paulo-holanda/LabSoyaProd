import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_squared_error
from scipy.stats import randint, uniform

class ModelTrainer:
    def __init__(self, X_train, X_test, y_train, y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def train(self):
        print("🧠 Treinando modelo ExtraTrees...")
        self.model = ExtraTreesRegressor(n_estimators=1500, max_depth=40,  min_samples_split=2, 
                                         min_samples_leaf=2, random_state=42, max_features=0.5,criterion='friedman_mse')
        # param_dist = {
        #     "n_estimators": randint(200, 2000),
        #     "max_depth": [None] + list(range(5, 41, 5)),
        #     "min_samples_split": randint(2, 50),
        #     "min_samples_leaf": randint(1, 20),
        #     "max_features": ["sqrt", "log2", 0.3, 0.5, 0.7, 1.0],
        #     "criterion": ["squared_error", "friedman_mse", "absolute_error", "poisson"],
        #     "bootstrap": [False, True],
        #     "max_samples": [None, 0.5, 0.7, 0.9, 1.0],  # será usado só se bootstrap=True
        #     "min_impurity_decrease": [0.0, 1e-7, 1e-4, 1e-3],
        #     "ccp_alpha": [0.0, 1e-4, 1e-3, 1e-2],
        # }

        # # Se for série temporal, prefira TimeSeriesSplit
        # cv = TimeSeriesSplit(n_splits=5)

        # search = RandomizedSearchCV(
        #     self.model,
        #     param_distributions=param_dist,
        #     n_iter=100,
        #     cv=cv,
        #     scoring="neg_mean_squared_error",
        #     n_jobs=-1,
        #     verbose=1,
        #     random_state=42
        # )

        # search.fit(self.X_train, self.y_train)
        # print(search.best_params_)
        # print(search.best_score_)
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        y_pred = self.model.predict(self.X_test)
        rmse = mean_squared_error(self.y_test, y_pred, squared=False)
        print(f"✅ RMSE: {rmse:.2f}")

    def predict(self, X_future: pd.DataFrame) -> pd.Series:
        """Usa o modelo treinado para prever produção de soja
        em um DataFrame de features já preparado."""
        return pd.Series(self.model.predict(X_future), index=X_future.index)

    def save(self, path="soja_model_et.pkl"):
        print(f"💾 Salvando modelo em {path}...")
        joblib.dump(self.model, path)

def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
    feat_imp_df = feat_imp_df.sort_values(by='importance', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(feat_imp_df['feature'], feat_imp_df['importance'])
    plt.gca().invert_yaxis()
    plt.title("Importância das variáveis (Extra Trees)")
    plt.tight_layout()
    plt.show()

