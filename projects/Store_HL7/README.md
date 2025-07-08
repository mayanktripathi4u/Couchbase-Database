Simulating the Real-World Healthcare System using two FastAPI applications.

1. The HL7v2 Source (e.g., EMR, Lab system) is one system that emits HL7 messages (over MLLP or REST). 
   Refer [EHR_System](/Couchbase-Database/projects/Store_HL7/EHR_System/)
2. The Ingestion & Storage App is a separate service that receives, parses, and stores the data.
    HL7v2 receiver + Couchbase writer (receives and stores parsed data).



```plaintext
                          ┌────────────────────────┐
                          │   HL7v2 / FHIR Source  │
                          │ (EMR, EHR, Lab system) │
                          └────────────┬───────────┘
                                       │
                                ┌──────▼──────┐
                                │ Ingestion   │
                                │ (API, MLLP) │
                                └──────┬──────┘
                                       │
                             ┌─────────▼──────────┐
                             │ Message Processor  │
                             │  (Python, FastAPI) │
                             └──────┬─────┬───────┘
               ┌───────────────────┘     └─────────────────────┐
       ┌──────▼────────┐                             ┌─────────▼────────┐
       │ Parse HL7/FHIR│                             │ Extract Metadata │
       │ into JSON     │                             │ (Patient ID, etc)│
       └──────┬────────┘                             └─────────┬────────┘
              │                                                │
   ┌──────────▼──────────┐                        ┌────────────▼────────────┐
   │ Store full message  │                        │ Index metadata in       │
   │ in Couchbase (JSON) │                        │ Elasticsearch (JSON doc)│
   └──────────┬──────────┘                        └────────────┬────────────┘
              │                                                │
    ┌─────────▼──────────┐                         ┌───────────▼────────────┐
    │ Couchbase UI / SDK │                         │ Kibana / Elastic APIs  │
    └────────────────────┘                         └────────────────────────┘

```

# Why Use Pydantic in FastAPI?
Pydantic is used for:

|Feature|	Benefit|
|--|--|
|Data Validation|	Ensures incoming request (e.g., JSON body) is valid|
|Automatic Type Checking|	Converts str, date, int correctly from input|
|OpenAPI generation|	Automatically generates request schemas for docs|
|Clean error messages|	Provides useful feedback if input is invalid|
|Security|	Prevents malformed/missing data from crashing app|

Pydantic simplifies and secures your input layer, especially for structured input (like patient info).

# Setup
```bash
cd /Users/tripathimachine/Desktop/Apps/GitHub_Repo/Couchbase-Database

conda create -n couchbase-venv python==3.10

conda activate couchbase-venv
```

# Start the EHR System
```bash
cd projects/Store_HL7/EHR_System
pip install -r requirements.txt

# Terminal - 1
# streamlit run streamlit_EHR_app.py

streamlit run streamlit_EHR_app_v2.py


# Terminal - 2
uvicorn fastapi_EHR_API:app --host 0.0.0.0 --port 8000 --reload

kill -9 $(lsof -ti:8000)
```

## What this does:
* Builds MSH + PID for all messages

* For ADT^A01 adds PV1 (visit), AL1 (allergies), and NTE (notes)

* For ORM^O01 adds ORC, OBR, and NTE

* For ORU^R01 adds OBR, multiple OBX, and NTE

* Allows entering multiple OBX segments

* Notes split by lines become multiple NTE segments

## Test FastAPI Only
Run in new Terminal, and make sure FastAPI is up and running (in differerent terminal). You should see:
```bash
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

# or
Uvicorn running on http://0.0.0.1:8000 (Press CTRL+C to quit)
```

Try sending a POST request manually using curl:
```bash
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"message": "MSH|^~\\&|Demo|Test|App|Dest|202406291200||ADT^A01|123|P|2.5\nPID|||12345||Doe^John||19900101|M|||"}'
```
If FastAPI works, it should respond with below.
```json
{"status":"received","length":...}
```
And your FastAPI console should print the message.


