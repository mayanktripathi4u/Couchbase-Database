## June 22, 2025
1️⃣ Understand What Couchbase Is
  * What to Learn: What is NoSQL? Why Couchbase vs others? When to use it?
  * Outcome: High-level understanding of why you're learning Couchbase.
* Refer [README](/Couchbase-Database/README.md) to understand it.

## June 23, 2025
Todays focus: Get Couchbase running locally using Docker, access the Web UI, create a bucket, and add your first document.

1️⃣ Install Couchbase (~~Locally or~~ via Docker)
* Do This First:
  * Install Docker if not already installed
  * Run Couchbase using Docker:
```bash
docker run -d --name couchbase \
  -p 8091-8096:8091-8096 -p 11210:11210 \
  couchbase:community
```
  * Open http://localhost:8091 in your browser
  * Goal: Access Couchbase Web UI, understand what Buckets, Scopes, and Collections are.

2️⃣ Concepts like Bucket, VBucket, Compression.

3️⃣ Summary of What I Complete Today:

|Task|	Status|
|--|--|
|🐳 Run Couchbase in Docker|	✅|
|🌐 Access Couchbase Web Console	|✅|
|📦 Create a bucket (demo-bucket)	|✅|
|🧾 Add a document manually	|✅|
|🔍 Run a simple N1QL query	|✅|
|📝 Save logs and notes in GitHub	|✅|
|Concepts|✅|

