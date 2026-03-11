FROM apache/hive:3.1.3

USER root

RUN apt-get update && apt-get install -y curl wget

RUN curl -L -o /opt/hive/lib/hadoop-aws-3.1.3.jar \
https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.1.3/hadoop-aws-3.1.3.jar && \
curl -L -o /opt/hive/lib/aws-java-sdk-bundle-1.11.901.jar \
https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar

RUN rm -f /opt/hive/lib/guava-*.jar
RUN wget -P /opt/hive/lib \
https://repo1.maven.org/maven2/com/google/guava/guava/27.0-jre/guava-27.0-jre.jar