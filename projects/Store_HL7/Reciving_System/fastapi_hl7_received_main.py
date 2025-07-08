from fastapi import FastAPI, Request
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.collection import InsertOptions
from datetime import datetime
import hl7
import uuid

app = FastAPI()

# Couchbase connection (adjust accordingly)
cluster = Cluster(
    'couchbase://localhost',
    ClusterOptions(PasswordAuthenticator('Administrator', 'password'))
)
bucket = cluster.bucket('hl7-data')
collection = bucket.default_collection()

@app.post("/ingest")
async def ingest_hl7(request: Request):
    raw_message = await request.body()
    hl7_str = raw_message.decode()

    try:
        h = hl7.parse(hl7_str)
        pid_segment = h.segment('PID')

        patient_id = pid_segment[3][0]
        name = pid_segment[5][0]
        dob = pid_segment[7][0]

        document = {
            "type": "hl7v2",
            "patient_id": patient_id,
            "name": name,
            "dob": dob,
            "hl7_raw": hl7_str,
            "received_at": datetime.utcnow().isoformat()
        }

        doc_id = f"hl7::{str(uuid.uuid4())}"
        collection.insert(doc_id, document)

        return {"message": "HL7v2 stored", "doc_id": doc_id}

    except Exception as e:
        return {"error": str(e)}


# To run the FastAPI app, use the command:
# CD into the directory containing this file and run:

# cd projects/Store_HL7/Reciving_System
# uvicorn fastapi_hl7_received_main:app --host 0.0.0.0 --port 9000 --reload

# Note: Ensure Couchbase is running and the bucket 'hl7-data' exists.
# You can create the bucket using the Couchbase Web Console or CLI.


# Trigger a simulated HL7 send:
# curl -X POST http://localhost:9000/send \
#   -H "Content-Type: application/json" \
#   -d '{"patient_id": "12345", "name": "John Doe", "dob": "1990-01-01"}'
