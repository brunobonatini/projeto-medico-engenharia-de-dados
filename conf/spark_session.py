from pyspark.sql import SparkSession
from conf.settings import settings

# Criação da seção do Spark
def get_spark_session(app_name: str = "ProjetoMedico") -> SparkSession:
    """
    Cria e retorna uma SparkSession configurada
    para Delta Lake + MinIO (S3A)
    """

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("spark://spark-master:7077")
        .config("spark.hadoop.fs.s3a.endpoint", settings.minio_endpoint)
        .config("spark.hadoop.fs.s3a.access.key", settings.minio_access_key)
        .config("spark.hadoop.fs.s3a.secret.key", settings.minio_secret_key)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.hadoop.hive.metastore.uris", "thrift://hive-metastore:9083")
        .config("spark.sql.debug.maxToStringFields", "5000")
        .config("spark.sql.shuffle.partitions", "200")
        .config("spark.executor.memory", "4g")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.files.maxPartitionBytes", "134217728")
        .enableHiveSupport()
        .getOrCreate()
    )

    return spark