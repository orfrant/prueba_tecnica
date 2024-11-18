from pyspark.sql import SparkSession
from sedona.spark import *
from sedona.core.SpatialRDD import SpatialRDD
from sedona.core.formatMapper.shapefileParser import ShapefileReader
from sedona.utils.adapter import Adapter

from sedona.register import SedonaRegistrator
from sedona.utils import SedonaKryoRegistrator, KryoSerializer
from pyspark.sql import functions as f

spark = SparkSession. \
    builder. \
    appName('appName'). \
    config("spark.serializer", KryoSerializer.getName). \
    config("spark.kryo.registrator", SedonaKryoRegistrator.getName). \
    config("spark.hadoop.fs.s3a.access.key", "AKIAX6JQ7KD3GQZZFGIK"). \
    config("spark.hadoop.fs.s3a.secret.key", "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"). \
    config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"). \
    config('spark.jars.packages',
           'org.apache.sedona:sedona-spark-shaded-3.5_2.12:1.6.1,'
           'org.datasyslab:geotools-wrapper:1.6.1-28.2,'
           'org.apache.hadoop:hadoop-aws:3.3.4'). \
    getOrCreate()

sedona = SedonaContext.create(spark)
pulsaciones = sedona.read.format("csv").options(header=True).load("s3a://pruebapulster/data/pulsaciones/PulsacionesPorDispositivo.csv")
pulsaciones = pulsaciones.withColumn(
    "geometry",
    ST_Point(f.col("Lon of Observation Point"), f.col("Lat of Observation Point"))
)

pulsaciones.count()

pulsaciones = pulsaciones.dropDuplicates()

pulsaciones = pulsaciones.withColumn("datetime", f.to_timestamp(f.concat(f.col('Date'), f.lit(' '), f.col('Time of Day'))))

pulsaciones.show()

comercios_rdd = ShapefileReader.readToGeometryRDD(sedona, "s3a://pruebapulster/shapes/Comercios/")
comercios = Adapter.toDf(comercios_rdd, sedona)

comercios.createOrReplaceTempView("comercios")
pulsaciones.createOrReplaceTempView("pulsaciones")

sedona.sql("select `Polygon Id`, count(*) from pulsaciones GROUP BY `Polygon Id`").show()

resultado = sedona.sql("""
    SELECT comercios.ARGOSCODE, count(*) as conteo FROM comercios, pulsaciones 
        WHERE ST_Contains(comercios.geometry, pulsaciones.geometry) 
        GROUP BY comercios.ARGOSCODE
    """)

resultado.show()

resultado.write.mode("overwrite").parquet("s3a://pruebapulster/data/resultados/conteo_pulsaciones")
