from data_loader import DataLoader

def save_semantic_layer(df):
    """Salva a camada de abstração no PostgreSQL."""
    loader = DataLoader()
    engine = loader.engine
    df.to_sql("semantic_layer", engine, index=False, if_exists = "replace")
