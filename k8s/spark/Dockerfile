FROM bitnami/spark:3.5.3
USER root
RUN apt-get update && apt-get install -y python3-pip wget

RUN pip install apache-sedona==1.6.1

RUN wget https://repo.maven.apache.org/maven2/org/datasyslab/geotools-wrapper/1.6.1-28.2/geotools-wrapper-1.6.1-28.2.jar  -P /opt/bitnami/spark/jars/
RUN wget https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-3.5_2.12/1.6.1/sedona-spark-shaded-3.5_2.12-1.6.1.jar -P /opt/bitnami/spark/jars/
