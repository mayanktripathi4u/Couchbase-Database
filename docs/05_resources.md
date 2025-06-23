## June 22, 2025
1️⃣ Understand What Couchbase Is
  * What to Learn: What is NoSQL? Why Couchbase vs others? When to use it?
  * Outcome: High-level understanding of why you're learning Couchbase.

## June 23, 2025
- Installed Couchbase via Docker
- Explored Web Console
- Read about Buckets and Documents


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

2️⃣ 