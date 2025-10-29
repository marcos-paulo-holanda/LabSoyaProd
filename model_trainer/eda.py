import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import shapiro

class ExploratoryDataAnalyzer:
    """
    Classe para análise exploratória de dados (EDA) de um DataFrame carregado do PostgreSQL.
    """
    def __init__(self, df):
        self.df = df.drop(columns=['id'])
        self.output_dir = os.path.join(os.path.dirname(__file__), "eda_outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze_missing_values(self):
        print("🔍 Analisando valores ausentes...")
        missing = self.df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if not missing.empty:
            missing.to_csv(os.path.join(self.output_dir, "missing_values.csv"))
            print(missing)
        else:
            print("Nenhum valor ausente encontrado.")

    def plot_univariate_distributions(self):
        """Gera gráficos de distribuição univariada (histogramas) para colunas numéricas do DataFrame.
        """
        print("📊 Gerando gráficos de distribuição univariada (histogramas)...")
        numeric_cols = self.df.select_dtypes(include=["float64", "int64"]).columns
        for col in numeric_cols:
            plt.figure(figsize=(8, 4))
            sns.histplot(self.df[col].dropna(), kde=True, color="#00CFC1")
            plt.title(f'Distribuição de {col}')
            plt.savefig(os.path.join(self.output_dir, f"univariate_dist_{col}.png"))
            plt.close()

    def plot_correlation_matrix(self):
        """Gera uma matriz de correlação para colunas numéricas do DataFrame e salva como imagem.
        """
        print("📈 Gerando matriz de correlação...")
        plt.figure(figsize=(12, 8))
        corr = self.df.corr(numeric_only=True)
        # Use #00CFC1 as the main color for the heatmap
        ax = sns.heatmap(
            corr,
            annot=True,
            cmap=sns.light_palette("#00CFC1", as_cmap=True),
            fmt=".2f",
            linewidths=0.5,
            cbar_kws={"label": "Correlação"}
        )
        plt.title('Matriz de Correlação')
        plt.tight_layout()  # Ajusta automaticamente para evitar cortes
        plt.savefig(os.path.join(self.output_dir, "correlation_matrix.png"), bbox_inches='tight')  # Garante que tudo caiba
        plt.close()

    def plot_pairplot(self):
        """Gera gráficos de distribuição para pares de variáveis numéricas.
        """
        print("🔗 Gerando pairplot para variáveis numéricas...")
        numeric_cols = self.df.select_dtypes(include=["float64", "int64"]).columns
        if len(numeric_cols) > 1:
            # Define a custom color palette using #00CFC1
            custom_palette = sns.color_palette(["#00CFC1"])
            sns.pairplot(
                self.df[numeric_cols].dropna(),
                diag_kind="kde",
                plot_kws={"color": "#00CFC1"},
                diag_kws={"color": "#00CFC1"},
                palette=custom_palette
            )
            plt.savefig(os.path.join(self.output_dir, "pairplot.png"))
            plt.close()
        else:
            print("Não há colunas numéricas suficientes para gerar o pairplot.")

    def plot_scatter(self):
        print("📉 Gerando gráficos distribuição bivariada com o scatter plot...")
        if 'production' not in self.df.columns:
            print("Coluna 'production' não encontrada no DataFrame.")
            return
        numeric_cols = self.df.select_dtypes(include=["float64", "int64"]).columns
        other_cols = [col for col in numeric_cols if col != 'production']
        for col in other_cols:
            plt.figure(figsize=(8, 6))
            plt.scatter(self.df[col], self.df['production'], color="#00CFC1", alpha=0.7)
            plt.xlabel(col)
            plt.ylabel('production')
            plt.title(f'Scatter plot: production vs {col}')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, f'scatter_production_vs_{col}.png'))
            plt.close()

    def plot_kde(self):
        print("📊 Gerando gráficos de distribuição bivariada com o KDE...")

        numeric_cols = self.df.select_dtypes(include=["float64", "int64"]).columns

        # Distribuições bivariadas para 'production' com todas as outras colunas numéricas
        if 'production' in numeric_cols:
            for other_col in numeric_cols:
                if other_col != 'production':
                    plt.figure(figsize=(8, 6))
                    sns.kdeplot(
                        data=self.df,
                        x=other_col,
                        y='production',
                        fill=True,
                        cmap='viridis',
                        levels=50,
                        thresh=0.05
                    )
                    plt.title(f'Distribuição KDE: production vs {other_col}')
                    plt.xlabel(other_col)
                    plt.ylabel('production')
                    plt.savefig(os.path.join(self.output_dir, f"kde_production_vs_{other_col}.png"))
                    plt.close()

    def check_normality(self, column):
        """
        Verifica se uma coluna segue uma distribuição normal usando o teste de Shapiro-Wilk.
        Salva o resultado em um arquivo de texto.
        """

        if column not in self.df.columns:
            print(f"Coluna '{column}' não encontrada no DataFrame.")
            return

        data = self.df[column].dropna()
        if len(data) < 3:
            print(f"Coluna '{column}' não possui dados suficientes para o teste de normalidade.")
            return

        stat, p_value = shapiro(data)
        result = (
            f"Teste de Shapiro-Wilk para '{column}':\n"
            f"Estatística: {stat:.4f}\n"
            f"p-valor: {p_value:.4f}\n"
        )
        if p_value > 0.05:
            result += "Provavelmente segue uma distribuição normal (falha em rejeitar H0).\n"
        else:
            result += "Provavelmente NÃO segue uma distribuição normal (rejeita H0).\n"

        print(result)
        with open(os.path.join(self.output_dir, f"normality_{column}.txt"), "w", encoding="utf-8") as f:
            f.write(result)


    def run(self):
        self.analyze_missing_values()
        self.plot_correlation_matrix()
        self.plot_univariate_distributions()
        self.plot_scatter()
        self.plot_kde()
        self.plot_pairplot()
        # self.check_normality('temperature_change')