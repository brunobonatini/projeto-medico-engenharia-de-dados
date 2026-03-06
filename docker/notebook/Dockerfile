FROM apache/spark:3.5.3

USER root

RUN apt-get update && apt-get install -y \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Jupyter
RUN pip install --no-cache-dir notebook==6.5.6

# Hadoop / AWS
RUN curl -L -o /opt/spark/jars/hadoop-aws-3.3.4.jar \
https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
curl -L -o /opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar \
https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

# Delta
RUN curl -L -o /opt/spark/jars/delta-spark_2.12-3.2.0.jar \
https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.2.0/delta-spark_2.12-3.2.0.jar && \
curl -L -o /opt/spark/jars/delta-storage-3.2.0.jar \
https://repo1.maven.org/maven2/io/delta/delta-storage/3.2.0/delta-storage-3.2.0.jar

COPY requirements-notebook.txt .
RUN pip install --no-cache-dir -r requirements-notebook.txt

WORKDIR /projeto

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token="]
