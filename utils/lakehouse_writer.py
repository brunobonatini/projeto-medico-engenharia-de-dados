# Função para padronizar o salvamento nas camadas do Data Lake
def write_delta(df, camada, tabela, mode="overwrite"):
    
    path = f"s3a://datalake/{camada}/{tabela}"
    
    (
        df.write
        .format("delta")
        .mode(mode)
        .option("overwriteSchema", "true")
        .save(path)
    )

    print(f"Tabela salva em: {path}")