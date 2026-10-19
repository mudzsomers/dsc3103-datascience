import time
import duckdb as db
from pyspark.sql import SparkSession, functions as F

BIG_PATH = "data/processed/prices_skewed.parquet"

def duckdb_job():
    t0 = time.perf_counter()
    result = db.sql(f"""
        SELECT market, AVG(price) AS mean_price, COUNT(*) AS n
        FROM '{BIG_PATH}'
        WHERE price IS NOT NULL
        GROUP BY market
        ORDER BY mean_price DESC
    """).df()
    elapsed = time.perf_counter() - t0
    print("=== DuckDB ===")
    print(result)
    print(f"Time: {elapsed:.3f}s")
    return elapsed

def spark_job():
    # Spin up a local Spark session utilizing all CPU cores (*)
    spark = (SparkSession.builder
             .appName("DSC3103")
             .master("local[*]")
             .getOrCreate())

    t0 = time.perf_counter()
    df = spark.read.parquet(BIG_PATH)

    # Perform the exact same analytical pipeline
    summary = (df.filter(F.col("price").isNotNull())
                 .groupBy("market")
                 .agg(F.avg("price").alias("mean_price"),
                      F.count("*").alias("n"))
                 .orderBy(F.col("mean_price").desc()))

    print("=== Spark plan ===")
    summary.explain()

    print("=== Spark result ===")
    summary.show()
    elapsed = time.perf_counter() - t0
    print(f"Time: {elapsed:.3f}s")


    print("=== Partitions and Skew ===")
    print("Partitions in input:", df.rdd.getNumPartitions())

    # How many rows does each market hold?
    df.groupBy("market").count().orderBy(F.col("count").desc()).show()

    # Repartition the DataFrame by market into 6 partitions
    repartitioned = df.repartition(6, "market")
    repartitioned.groupBy(F.spark_partition_id().alias("pid")).count().show()

    print(f"Time: {elapsed:.3f}s")

    spark.stop()
    return elapsed
def spark_cache_job(use_cache):
    spark = SparkSession.builder.master("local[*]").appName("cache").getOrCreate()
    
    # Filter the dataset down to just 'Maize'
    df = spark.read.parquet(BIG_PATH).filter(F.col("commodity") == "Maize")

    if use_cache:
        df = df.cache()

    t0 = time.perf_counter()
    
    # Action 1: Group by market and get average price
    df.groupBy("market").agg(F.avg("price")).collect()     
    
    # Action 2: Group by market and get average rainfall
    df.groupBy("market").agg(F.avg("rainfall_mm")).collect()   
    
    elapsed = time.perf_counter() - t0

    print(f"use_cache={use_cache}: {elapsed:.3f}s")
    spark.stop()
    return elapsed


if __name__ == "__main__":
    #print("Running DuckDB baseline...")
    #duckdb_time = duckdb_job()
    
    #print("\nRunning PySpark job...")
    #spark_time = spark_job()


    #if __name__ == "__main__":
    print("Running DuckDB baseline...")
    duckdb_job()
    
    print("\nRunning PySpark job...")
    spark_job()
    
    print("\nRunning Spark Cache Evaluation...")
    print("--- Test 1: Without Cache ---")
    spark_cache_job(use_cache=False)
    
    print("--- Test 2: With Cache ---")
    spark_cache_job(use_cache=True)


