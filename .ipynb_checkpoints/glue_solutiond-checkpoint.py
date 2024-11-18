%pip install apache-sedona==1.6.1

%%configure -f
{
    "conf": {
        "spark.jars.packages": "org.apache.sedona:sedona-spark-shaded-3.0_2.12:1.6.1,org.datasyslab:geotools-wrapper:1.6.1-28.2"
    }
}

from sedona.spark import *
from sedona.core.SpatialRDD import SpatialRDD
from sedona.core.formatMapper.shapefileParser import ShapefileReader
from sedona.utils.adapter import Adapter
from pyspark.sql.functions import col
from pyspark.sql import functions as f

sedona = SedonaContext.create(spark)

pulsaciones = sedona.read.format("csv").options(header=True).load("s3://pruebapulster/data/pulsaciones/*.csv")
pulsaciones = pulsaciones.withColumn(
    "geometry",
    ST_Point(col("Lon of Observation Point"), col("Lat of Observation Point"))
)

pulsaciones.count()

pulsaciones = pulsaciones.dropDuplicates()

pulsaciones = pulsaciones.withColumn("datetime", f.to_timestamp(f.concat(f.col('Date'), f.lit(' '), f.col('Time of Day'))))

pulsaciones.show()

comercios_rdd = ShapefileReader.readToGeometryRDD(sedona, "s3://pruebapulster/shapes/Comercios/")
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

resultado.write.mode("overwrite").parquet("s3://pruebapulster/data/resultados/conteo_pulsaciones")

import os

os.system("jupyter nbconvert --to script glue_solutiond.ipynb")


