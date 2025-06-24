# Notes from Youtube Channels and Other resources.

Couchbase is NoSQL Database.
It supports
- Semi-Structure data such as
  - JSON data
  - Binary Data
- Works on Key-Value paris concept.
  - Key is 
  - Value could be the entire JSON Document or single value.

**Features / Benefits of Couchbase**
1. [Memory First Architecture](/Couchbase-Database/docs/01_overview.md#1--memory-first-architecture).
    Couchbase database follow memory (RAM) first architecure, which means for any write operation data first goes to RAM / Memory and then replicates to Disk. 
2. Distributed Database

3. Scalability
    Easily scale Horizontally by adding more nodes.

4. Fault-Tolerance

**Data**
- JSON Document
- Key-Value
- Flexible schema
- Dynamic add or remove schema
- N1QL for query (run sql like query to fetch data)

**Bucket**
- Consider kind of Database when compared to Relational Database.
- Limit to 10 Buckets in complete couchbase server / cluster.

**VBuckets**
- For each bucket, there will be 1024 virtual buckets as a default. Internally created by Couchbase.
- These VBuckets are distributed in each clusters. 

**Compression**
- Option to enable compression in Memory.
- Save the data in compressed format in RAM to reduce the data size.
- Disk will always saves in compressed format.

**Expiration**
- Time to Live (TTL) determines how long the data to retain and then expire or delete.
- 

**Scenario**
1. what happens when the RAM / Memory is full and a new document arrives?
    As we learned that Couchbase is Memory-First, any incoming data will first goes into memory and staty there. 
    Now we already added "n" documents and the "n" is so huge that our RAM is all full across all nodes in your cluster. So what will happen when a new document (K n+1 & V n+1) arrives.
    One of the document will get ejected from the RAM and is written / asaved into the Disk. With this a space is created for "n+1"th document.

    How this document is selected -- The less frequent used document. 




Example:
```json

```