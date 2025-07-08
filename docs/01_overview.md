# 📌 What is Couchbase Database?
In layman terms, Couchbase is like a super-fast digital filing cabinet. Instead of putting your documents (data) into fixed folders (tables and columns like in traditional databases), you can drop in flexible documents (called JSON documents) where each can look a bit different. It's like organizing files in a way that doesn't force every file to follow the same template.

Couchbase is like a super-fast, flexible digital cabinet that stores your information as smart files (JSON), easy to change, easy to find, and always ready — whether you're building a mobile app, a game, or a global e-commerce platform. It’s not meant for deep data analysis but is perfect for real-time operations.

# 📌 Why is it used?
Couchbase is used when:

* You need real-time performance (e.g., gaming, e-commerce, mobile apps).

* Your data structure is changing often or is unstructured.

* You want to scale easily (e.g., millions of users worldwide).

* You need offline + online sync (especially for mobile apps).

* You need high availability and replication across servers or geographies.

## 📌 Why Couchbase?

Couchbase is a modern, distributed NoSQL database optimized for high performance, scalability, and flexibility. It supports flexible JSON documents, SQL-like querying (N1QL), built-in caching, and real-time mobile sync — making it ideal for modern apps.


# 🔹 How is it different from other databases?
If you have every worked in any other databases, then you might have this question, how Couchbase database is different from that specific database I have worked or working.

|Feature|	Couchbase|	Traditional RDBMS (e.g., MySQL)	|MongoDB (another NoSQL DB)|
|--|--|--|--|
|Type	|NoSQL (Document Store + Key-Value)	|Relational (SQL-based)|	NoSQL (Document Store)|
|Schema|	Flexible (schema-less)	|Rigid (pre-defined schema)	|Flexible|
|Performance	|Very high (built-in cache)	|Moderate	|High|
|Scaling	|Horizontally scalable	|Hard to scale |horizontally	Scalable|
|Query Language	|N1QL (SQL-like for JSON)	|SQL	|Mongo Query Language
|Built-in Cache	|Yes (key differentiator)	|No	|No
|Mobile Sync	|Yes (Couchbase Mobile)	|No	|Some support


# 🔹 Is Couchbase OLTP or OLAP?
✅ OLTP (Online Transaction Processing) — Couchbase is best used for fast, frequent read/write operations like in:

* User profiles

* Shopping carts

* Real-time data sync

* Mobile app data

> 🚫 Not designed primarily for OLAP (Online Analytical Processing) or deep analytical queries. You’d typically use a separate system for that, like a data warehouse.

> ✅ Database → Yes, Couchbase is a NoSQL operational database.

> ❌ Data Warehouse → No, it's not built for large-scale batch analytics or BI dashboards.

> ❌ Data Lake → No, it doesn't store unstructured raw data in massive volume like Hadoop or S3.

# 🧱 Architecture Overview
Understanding Couchbase’s architecture will give us clarity on how it's built for performance, scalability, and flexibility.

Couchbase uses a modular and distributed architecture with specialized services.

## 1. 🧠 Memory-First Architecture
Couchbase's memory-first architecture is one of its key performance advantages, and it’s different from many traditional databases.

Memory-first means that reads and writes go to RAM (memory) first, not directly to disk. This makes operations much faster compared to disk-first databases.

### 💡 How It Works in Couchbase
#### 🔁 Write Flow:
1. When you write a document:

   * It goes into managed cache (RAM).

   * It is then asynchronously persisted to disk (eventually).

   * You get a fast response because you're not waiting on disk I/O.

2. The document is also added to a replica on another node if configured.

#### 👓 Read Flow:
1. When you read a document:

   * Couchbase checks the in-memory cache first.

   * If it’s there → instant response.

   * If not → it fetches from disk and optionally caches it again.

### Why it matters?
| Benefit                              | Description                                                                |
| ------------------------------------ | -------------------------------------------------------------------------- |
| ⚡ **High Speed**                     | RAM access is much faster than disk access.                                |
| 🔁 **Non-blocking Writes**           | Writes don’t block because disk operations are async.                      |
| 🚫 **Avoids Cache Layer Complexity** | You don’t need to add Redis or Memcached separately — caching is built-in. |
| 📉 **Lower Latency**                 | Ideal for real-time apps (e.g., gaming, chat, dashboards).                 |


### 🛠️ Optional Durability Settings
You can control how strict Couchbase is with persistence and replication:

   * For fast writes: accept RAM write only.

   * For strong durability: wait until it’s persisted to disk or replicated.

**In-short**
   * Couchbase's memory-first architecture means:

   * All reads and writes are performed in RAM first.

   * Disk is used for durability, not performance.

   * Built-in cache eliminates the need for external caching layers like Redis or Memcached.


## 2. Cluster-Based Design
A Couchbase cluster is made of one or more nodes (servers).

Each node can run one or more services.

## 3. Core Services in Couchbase
| Service               | Role                                                     |
| --------------------- | -------------------------------------------------------- |
| **Data Service**      | Stores and manages JSON documents in memory and on disk. |
| **Query Service**     | Processes N1QL queries (like SQL engine).                |
| **Index Service**     | Maintains indexes for fast query execution.              |
| **Search Service**    | Provides full-text search capability.                    |
| **Analytics Service** | Used for OLAP-style queries (batch/aggregates).          |
| **Eventing Service**  | Triggers functions on data changes.                      |
| **Backup Service**    | Manages backup and restore operations.                   |


Services can be colocated or isolated (e.g., you may have nodes that only handle queries).

## 4. Smart Client Architecture
Couchbase SDK clients (Python, Java, etc.) are "smart clients".

They know where each document lives in the cluster — reducing the need for intermediaries like load balancers.

Makes reads/writes faster and more efficient.

## 5. Data Distribution with vBuckets
Documents are hashed and assigned to vbuckets (logical partitions).

vbuckets are evenly distributed across nodes.

If a node goes down, its vbuckets are reassigned automatically.

## 6. XDCR (Cross Data Center Replication)
Lets you replicate data from one cluster to another — great for disaster recovery, backups, or geo-distributed apps.


# Features
Understanding Couchbase’s features will give us clarity on how it's built for performance, scalability, and flexibility.

| Feature                                 | Explanation                                                                                                         |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 🧾 **JSON Document Store**              | Stores data in flexible JSON format. No rigid schema — every document (record) can have different fields.           |
| ⚡ **High Performance (Built-in Cache)** | Couchbase has an integrated memory-first architecture (via *managed cache*) so data can be read/written super fast. |
| 📊 **N1QL Query Language**              | SQL-like language to query JSON documents. Easy for SQL users to pick up.                                           |
| ⚖️ **Horizontal Scalability**           | You can add more nodes to scale out — useful for handling high user loads or large data volumes.                    |
| 🌐 **Distributed Architecture**         | Data is distributed across multiple nodes — built for fault tolerance and reliability.                              |
| 🔁 **Replication & High Availability**  | Built-in cross-datacenter replication (XDCR) ensures that if one node fails, others take over seamlessly.           |
| 📱 **Mobile Sync (Sync Gateway)**       | Allows mobile apps to work offline and sync back to Couchbase when online. Ideal for real-time mobile apps.         |
| 🔐 **Security**                         | Role-based access control, data encryption, auditing, LDAP/SSO integration.                                         |
| 🛠️ **SDKs for Multiple Languages**     | Supports Python, Java, Go, Node.js, C#, etc., making it developer-friendly.                                         |
| ☁️ **Hybrid Deployment**                | Can be deployed on-prem, in the cloud, or hybrid. Works well with Docker and Kubernetes.                            |
| 🧩 **Eventing and Functions**           | Supports serverless-like event handling (e.g., when document changes, trigger a function).                          |
| 📥 **Flexible Indexing**                | Supports primary, secondary, array, and full-text search indexes for fast query performance.                        |


# Bucket
- Bucket is logical structure on the cluster.
- Each bucket has 1024 vBuckets (Shards)
- Data spread evenly acorss the cluster (with rebalance).
- Each key is mapped to a vBucket on a node.
- Types of Bucket:
  - Couchbase
  - Memcached
  - Ephemeral
- Memory Quota: Define Memory Quota in MB per server node. Once defined say as 100 MB, it will get multipled with the count of Nodes with Data Services.

## Add a Bucket (From Web-UI)
- Name: a unique name for a bucket.
- Memory Quota
- Bucket Type
- Replicas
  - Enable with "n" number of replica (backup) copies. Note these are count of copies. If set 1 then there will be one main and one backup copy. When set Replicas as 2, it will be total of 3 sets (one main and 2 rbackup copy). Its recommended to have one Replica when you have 3 nodes in your COuchbase Cluster. When you have 5 Nodes in your CLuster then go with 2 Replicas, and if you have more than 5 nodes in your cluster than go with 3 replicas.
  
  - Replicate view indexes.
-  Bucket Max Time-To-Live
   -  Enable it with 60 seconds
-  Compression Mode
   -  Off => Compressed documents are accepted but actively decompressed for storage in memory and for streaming. Not advised.
   -  Passive => Compressed documents can be stored and streamed from the server, but the server does not try to actively compress documents (Client-Initiated).
   -  Active => The server will try to actively compress documents in memory.
-  Conflict Resolution: Is used when using XCDR. 
   -  Sequence Number
   -  Timestamp
   Choose the `timestamp` conflict resolution method if XCDR replications will be set up for this bucket. Attention: `timestamp` conflict resolution requires additional NTP setup.

-  Ejection Method
   -  Value-only: During ejection, only the value will be ejected (key and metadata will remain in memory). This needs more system memory. But provides the best performance.
   -  Full: During ejection. everything (inclduing key, metadata and value) will be ejected. It reduces the memory iverhead requirement.

-  Bucket Priority
    This allows tasks to be handled based on priority. The effect is relative between buckets. If all buckets are set to "high" then no bucket will have priority over another.
   -  Default: 
   -  High: 
-  Auto-Compaction
   -  Override the default auto-compaction settings
-  Flush
   -  Enable
-  

## Add Bucket (Using CLI)
For this navigate to Terminal (on installed machive or VM)
```bash
couchbase-cli bucket-create -c 192.168.0.1:8091 \
--username Administrator \
--password password \
--bucket my-bucket \
--bucket-type couchbase \
--bucket-ramsize 512 \
--bucket-replica 2 \
--bucket-priority high \
--bucket-eviction-policy fullEviction \
--enable-flush 1 \
--enable-index-replica 1
```

