from pyspark.sql import SparkSession
from conf.settings import settings
from delta import configure_spark_with_delta_pip

# Função para criação da sessão do Spark
def get_spark_session(app_name: str = "Projeto-Medico") -> SparkSession:

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("spark://spark-master:7077")

        # MinIO (S3)
        .config("spark.hadoop.fs.s3a.endpoint", settings.minio_endpoint)
        .config("spark.hadoop.fs.s3a.access.key", settings.minio_access_key)
        .config("spark.hadoop.fs.s3a.secret.key", settings.minio_secret_key)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")

        # Delta Lake
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.databricks.delta.schema.autoMerge.enabled", "true")

        # Hive Metastore
        .config("spark.sql.catalogImplementation", "hive")
        .config("spark.hadoop.hive.metastore.uris", "thrift://hive-metastore:9083")
        .enableHiveSupport()

        # Hive Warehouse
        .config(
            "spark.sql.warehouse.dir",
            f"s3a://{settings.minio_bucket}/warehouse"
        )

        # Performance
        .config("spark.sql.shuffle.partitions", "200")
        .config("spark.executor.memory", "4g")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.files.maxPartitionBytes", "134217728")
        .config("spark.sql.debug.maxToStringFields", "5000")
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    return spark