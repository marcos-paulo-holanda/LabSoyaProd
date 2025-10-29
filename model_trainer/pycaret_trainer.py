
from pycaret.regression import setup, compare_models, finalize_model, predict_model, save_model

class PyCaretTrainer:
    def __init__(self, df, target='Production'):
        self.df = df
        self.target = target
        self.best_model = None
        self.final_model = None

    def setup_experiment(self):
        print("🔧 Inicializando experimento do PyCaret...")
        setup(
            data=self.df,
            target=self.target,
            train_size=0.8,
            session_id=42,
            remove_multicollinearity=True,
            multicollinearity_threshold=0.9,
            use_gpu=True
        )

    def compare_models(self):
        print("🤖 Comparando modelos...")
        self.best_model = compare_models()
        print("✅ Melhor modelo:", self.best_model)

    def finalize_model(self):
        print("📦 Finalizando modelo com todo o conjunto de dados...")
        self.final_model = finalize_model(self.best_model)

    def save(self, path='modelo_producao_soja'):
        print(f"💾 Salvando modelo em {path}.pkl")
        save_model(self.final_model, path)

    def run(self):
        self.setup_experiment()
        self.compare_models()
        self.finalize_model()
        # self.save()
