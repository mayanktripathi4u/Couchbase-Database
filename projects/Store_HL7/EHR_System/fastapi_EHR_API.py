from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()

class HL7Message(BaseModel):
    message: str


@app.post("/ingest")
async def ingest_hl7(payload: HL7Message):
    print("📥 Received HL7 Message:")
    print(payload.message.replace("\n", "\n   "))  # Pretty print
    return JSONResponse(content={"status": "received", "length": len(payload.message)})


# To run the FastAPI app, use the command:
# uvicorn fastapi_EHR_API:app --host 0.0.0.0 --port 8000 --reload
# Note: Ensure the EHR system's ingest endpoint is running and accessible at the specified URL.
# You can test the endpoint using a tool like Postman or curl.

