FROM apache/spark:3.5.3

USER root

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# Hadoop AWS
RUN curl -L -o /opt/spark/jars/hadoop-aws-3.3.4.jar \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    curl -L -o /opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

# Delta Lake
RUN curl -L -o /opt/spark/jars/delta-core_2.12-3.2.0.jar \
    https://repo1.maven.org/maven2/io/delta/delta-core_2.12/3.2.0/delta-core_2.12-3.2.0.jar && \
    curl -L -o /opt/spark/jars/delta-storage-3.2.0.jar \
    https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar

# Configurações Spark
RUN mkdir -p /opt/spark/conf && \
    echo "spark.hadoop.fs.s3a.endpoint=${MINIO_ENDPOINT}" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.access.key=${MINIO_ACCESS_KEY}" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.secret.key=${MINIO_SECRET_KEY}" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.path.style.access=true" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.connection.ssl.enabled=false" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" >> /opt/spark/conf/spark-defaults.conf && \
    echo "spark.databricks.delta.schema.autoMerge.enabled=true" >> /opt/spark/conf/spark-defaults.conf

COPY requirements-spark.txt .
RUN pip3 install --no-cache-dir -r requirements-spark.txt

WORKDIR /projeto

CMD ["/bin/bash"]
