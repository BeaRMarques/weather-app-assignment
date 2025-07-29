"""
Reads stream from kafka topic, processes it and writes it to PostgreSQL.
"""

import logging
import sys
import time

from constants import (
    KAFKA_BOOTSTRAP_SERVER,
    KAFKA_TOPIC_NAME,
    POSTGRES_DB,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TABLE,
    POSTGRES_URL,
    POSTGRES_USER,
)
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, current_timestamp, explode, from_json, sum
from pyspark.sql.types import (
    ArrayType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

input_schema = StructType(
    [
        StructField("lat", FloatType(), nullable=False),
        StructField("lon", FloatType(), nullable=False),
        StructField("timezone", StringType(), nullable=False),
        StructField("timezone_offset", IntegerType(), nullable=False),
        StructField(
            "minutely",
            ArrayType(
                StructType(
                    [
                        StructField("dt", IntegerType(), nullable=False),
                        StructField("precipitation", FloatType(), nullable=False),
                    ]
                )
            ),
            nullable=False,
        ),
    ]
)


def write_to_postgres(batch_df: DataFrame, batch_id: int) -> None:
    """Writes each batch to postgres."""
    return (
        batch_df.write.format("jdbc")
        .option(
            "url", f"jdbc:postgresql://postgresql:{POSTGRES_PORT}/{POSTGRES_DB}"
        )  # jdbc:postgresql://localhost:5432
        .option("dbtable", "precipitation_location")
        .option("user", POSTGRES_USER)
        .option("password", POSTGRES_PASSWORD)
        .option("driver", "org.postgresql.Driver")
        .mode("append")
        .save()
    )


def read_stream() -> DataFrame:
    """Initializes spark session and reads stream from kafka topic."""
    spark_session = (
        SparkSession.builder.appName("StreamReader")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.6.0",
        )
        .getOrCreate()
    )

    return (
        spark_session.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
        .option("subscribe", KAFKA_TOPIC_NAME)
        .load()
    )


def process_stream(df_raw: DataFrame) -> DataFrame:
    """Parses and aggregates streaming data from DataFrame."""
    df_raw = df_raw.selectExpr(
        "CAST(value AS STRING) as dict_str", "timestamp as ingestion_time"
    )
    df_parsed = df_raw.select(
        from_json("dict_str", input_schema).alias("data"), "ingestion_time"
    ).select("data.*", "ingestion_time")

    df_exp = df_parsed.withColumn("minutely", explode("minutely"))

    df_agg = (
        df_exp.withWatermark("ingestion_time", "10 seconds")
        .groupBy("lat", "lon", "ingestion_time")
        .agg(sum("minutely.precipitation").alias("total_precipitation"))
    )

    return df_agg


logger.debug("Reading Kafka stream.")
df = read_stream()

logger.debug("Processing Kafka stream.")
df_final = process_stream(df)

logger.debug("Sending stream to Postgres.")
query = (
    df_final.writeStream.foreachBatch(write_to_postgres).outputMode("append").start()
)
query.awaitTermination()
