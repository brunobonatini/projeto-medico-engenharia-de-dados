# Função para padronizar o salvamento nas camadas do Data Lake
def write_delta(df, camada, tabela, mode="overwrite"):

    path = f"s3a://datalake/{camada}/{tabela}"

    writer = (
        df.write
        .format("delta")
        .mode(mode)
    )

    if mode == "append":
        writer = writer.option("mergeSchema", "true")

    if mode == "overwrite":
        writer = writer.option("overwriteSchema", "true")

    writer.save(path)