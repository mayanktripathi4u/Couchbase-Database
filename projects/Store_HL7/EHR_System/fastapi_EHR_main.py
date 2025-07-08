from fastapi import FastAPI
import requests
import hl7
from pydantic import BaseModel 


app = FastAPI()

class SimInput(BaseModel):
    patient_id: str
    name: str
    dob: str

@app.post("/send")
# def send_hl7(input: SimInput):
def send_hl7():
    # Simulated HL7v2 message string
    hl7_msg = f"""MSH|^~\\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|202406281234||ADT^A01|MSG00001|P|2.5
PID|||{input.patient_id}||{input.name}||{input.dob}|M|||
"""
    print(f"HL7 Message (string): {hl7_msg}")
    
    # Convert the HL7 message string to an HL7 object
    hl7_msg = hl7_msg.encode('utf-8')  # Encode the HL7 message to bytes

    print(f"HL7 Message (bytes): {hl7_msg}")
    # Send the HL7 message to the EHR system's ingest endpoint
    response = requests.post("http://localhost:8000/ingest", data=hl7_msg)
    return {"status": response.status_code, "response": response.json()}


# To run the FastAPI app, use the command:
# uvicorn fastapi_EHR_main:app --host 0.0.0.0 --port 8000 --reload
# Note: Ensure the EHR system's ingest endpoint is running and accessible at the specified URL.
# You can test the endpoint using a tool like Postman or curl.

