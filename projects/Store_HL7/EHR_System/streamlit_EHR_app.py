import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Simulated EHR System", layout="centered")
st.title("🧪 HL7v2 Message Sender (Simulated EHR)")

# Mapping of message types to valid trigger events
msg_event_map = {
    "ADT": ["A01", "A03", "A04", "A08"],
    "ORM": ["O01"],
    "ORU": ["R01", "R03"],
    "DFT": ["P03", "P05"]
}

# # ---- Form ----
# with st.form("hl7_form"):
#     name = st.text_input("Patient Name (e.g., JOHN DOE)")
#     patient_id = st.text_input("Patient ID", "12345")
#     dob = st.date_input("Date of Birth", datetime.date(1990, 1, 1))
#     # msg_type = st.selectbox("Message Type", ["ADT", "ORM", "ORU"])
#     # trigger_event = st.selectbox("Trigger Event", ["A01", "A03", "O01", "R01"])

#     # msg_type = st.selectbox("Message Type", list(msg_event_map.keys()))
#     msg_type = st.selectbox("Message Type", list(msg_event_map.keys()), key="msg_type")

#     # Access the current selected msg_type from session_state
#     current_msg_type = st.session_state.msg_type

#     st.write(f"Selected Message Type: {msg_type}")
#     # Dynamic event list based on selected type
#     # trigger_event = st.selectbox("Trigger Event", msg_event_map[msg_type])
#     trigger_event = st.selectbox("Trigger Event", msg_event_map[current_msg_type], key="trigger_event")


#     submit = st.form_submit_button("Send Message")

# st.write(f"Selected Message Type: {st.session_state.msg_type}")
# st.write(f"Selected Trigger Event: {st.session_state.trigger_event}")


# --- Without Form to support dynamic dependent selectbox ---
name = st.text_input("Patient Name (e.g., JOHN DOE)")
patient_id = st.text_input("Patient ID", "12345")
dob = st.date_input("Date of Birth", datetime.date(1990, 1, 1))

msg_type = st.selectbox("Message Type", list(msg_event_map.keys()), key="msg_type")

# Access the current selected msg_type from session_state
current_msg_type = st.session_state.msg_type

# st.write(f"Selected Message Type: {msg_type}")

# Dynamic event list based on selected type
trigger_event = st.selectbox("Trigger Event", msg_event_map[current_msg_type], key="trigger_event")

# ---- Process ----

# if st.button("Submit"):
#     st.write(f"Selected: {msg_type} ^ {trigger_event}")

# if submit:
if st.button("Submit"):
    dob_str = dob.strftime("%Y%m%d")
    hl7_msg = f"""MSH|^~\\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|202406281234||{msg_type}^{trigger_event}|MSG00001|P|2.5
PID|||{patient_id}||{name}||{dob_str}|M|||
"""

    # Send to receiver
    try:
        # response = requests.post("http://localhost:8000/ingest", data=hl7_msg)
        st.success("Message sent!")
        st.code(hl7_msg, language="hl7")
        # st.json(response.json())
    except Exception as e:
        st.error(f"Failed to send: {e}")



# """
# How to run:
# cd projects/Store_HL7/EHR_System
# streamlit run streamlit_EHR_app.py
# """