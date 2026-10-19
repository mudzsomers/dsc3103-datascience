# Lab 6 Notes

## Step 1 — Create a bigger, skewed dataset
**Question:** What share of the rows belongs to Owino now, and why did we do this on purpose?

**Answer:** 
* 
C:\Users\DELL LATITUDE 5480\Documents\dsc3103-project\dsc3103-project>python src/scale/skewed_data.py
market
Owino       0.700
Nakasero    0.063
Bwaise      0.062
Kansanga    0.061
Unknown     0.058
mukono      0.056
Name: proportion, dtype: float64
Wrote data/processed/prices_skewed.parquet rows: 5000000
 70% (0.700) of the total rows now belong to "Owino".
* Purpose: This creates a conscious data skew. It allows us to observe how a distributed engine like Spark handles heavily unbalanced partitions compared to a single-node engine like DuckDB.
 ## Step 3 — The same job in Spark
**Question 1:** Which was faster, DuckDB or Spark? Roughly by how much?
**Answer:** DuckDB was faster than Spark. It completed the job in 1.309s compared to Spark's 9.780s, making DuckDB roughly 7.5 times faster for this local 5M row dataset.

**Question 2:** Nothing happened when `summary = ...` was executed. Which line actually triggered the work, and why?
**Answer:** The line `summary.show()` triggered the actual execution. In Spark, operations like `.filter()`, `.groupBy()`, and `.orderBy()` are **transformations**, which are evaluated lazily. The work is only executed when an **action** like `.show()` or `.explain()` is called.

## Step 4 — Read the plan
**Question 1:** Which of your operations caused the `Exchange` (shuffle)? Was it `filter`, `groupBy`, or `orderBy`?
**Answer:** Both `groupBy` and `orderBy` caused an `Exchange`. The plan shows a `hashpartitioning` exchange for the group-by operation and a `rangepartitioning` exchange for the sort order operation.

**Question 2:** Is `filter` narrow or wide? Is `groupBy` narrow or wide?
**Answer:** 
* `filter` is a **narrow** transformation because it processes data within a single partition without moving records between workers.
* `groupBy` is a **wide** transformation because it requires an `Exchange` to shuffle matching keys across different partitions.

**Question 3:** Which line of the plan shows Spark only reading the columns it needs?
**Answer:** The `FileScan parquet` line at the very bottom shows Spark optimizing the read schema: `ReadSchema: struct<market:string,price:bigint>`. It only reads the `market` and `price` columns from the Parquet file.


## Step 5 — Partitions and skew
**Question 1:** After repartitioning by `market`, how uneven are the partition sizes?
**Answer:** The partition sizes are heavily uneven. While partitions 0, 1, and 5 hold around 280,000 to 314,000 rows each, partition 2 holds 4,088,959 rows due to the 70% data skew introduced for "Owino". Two partitions out of the requested six ended up completely empty.

**Question 2:** In a real cluster, which worker would finish last, and what does that do to total job time?
**Answer:** The worker assigned to partition 2 would finish last. Because a stage in Spark is only as fast as its slowest task, this single bottleneck worker will keep the entire cluster waiting, significantly slowing down the total job time and wasting cluster resources.

## Step 6 — Cache or not?
**Question:** Did caching help? Would it help if only ONE action were run on `df`? Explain.

**Answer:** 
* Caching did not help. It made the job significantly slower, increasing execution time from 2.808s to 7.593s. Caching has an upfront overhead because Spark must write the serialized data partitions into memory/disk. Since this 5-million-row subset fits easily into the OS page cache anyway, reading it from memory memory-overhead costs more than just reading the raw parquet file twice.
* If only one action were run on `df`, caching would be completely useless and would only add unnecessary performance overhead. Caching is exclusively beneficial when the same filtered/transformed DataFrame is reused across multiple iterative actions downstream.


## Step 7 — Decision memo

### Performance Evaluation Summary

| Job | Time (s) |
|---|---|
| DuckDB, 5M rows | 0.994s |
| Spark local, 5M rows | 9.332s |
| Spark without cache (2 actions) | 2.808s |
| Spark with cache (2 actions) | 7.593s |

---

### Recommendations

#### Scenario A: Weekly report on 500,000 rows stored in one Parquet file
* **Recommendation:** DuckDB
* **Justification:** DuckDB is highly optimized for single-node, analytical operations on files that fit easily within local machine memory. Given that it handled 5,000,000 rows in less than a second, a dataset of 500,000 rows will process almost instantly without any cluster coordination overhead.

#### Scenario B: 2 TB of mobile-money transaction logs processed nightly with fault-tolerance requirements
* **Recommendation:** Apache Spark
* **Justification:** This scenario requires processing a massive volume of data that exceeds single-node storage and memory limits. Spark is built for distributed environments, allowing data processing to scale across multiple worker nodes. Its lineage-graph structure ensures robust fault tolerance, meaning the job can automatically recover and resume tasks if specific machine nodes fail during operation.

#### Scenario C: A 3 GB file on a laptop with 16 GB of RAM
* **Recommendation:** DuckDB
* **Justification:** A 3 GB file can fit entirely into the laptop's 16 GB of RAM. DuckDB processes this file locally using highly efficient vectorized execution directly on the CPU cores. Running Spark locally in this setup introduces unnecessary Java Virtual Machine (JVM) initialization and communication overhead, which wastes memory resources and degrades execution speed.

