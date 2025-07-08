import streamlit as st
import datetime
import requests

# Helper to format dates as HL7 (YYYYMMDD or YYYYMMDDHHMMSS)
def hl7_date(dt, include_time=False):
    if include_time:
        return dt.strftime("%Y%m%d%H%M%S")
    return dt.strftime("%Y%m%d")

def generate_message_control_id():
    return "MSG" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

# Build MSH segment (basic)
def build_msh(msg_type, trigger_event):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    msg_ctrl_id = generate_message_control_id()
    return f"MSH|^~\\&|Streamlit-EHR|Streamlit-Facility|Receiving-Couchbase-App|ReceivingFacility|{timestamp}||{msg_type}^{trigger_event}|{msg_ctrl_id}|P|2.5"


def input_adt_a01():
    st.subheader("ADT^A01 - Admit Patient")
    pid = st.text_input("Patient ID")
    name = st.text_input("Patient Name")
    dob = st.date_input("Date of Birth", datetime.date(1990, 1, 1))
    admit_date = st.date_input("Admit Date", datetime.date.today())
    allergies = st.text_area("Allergies")
    notes = st.text_area("Nurse Notes")
    return dict(pid=pid, name=name, dob=dob, admit_date=admit_date, allergies=allergies, notes=notes)

def input_orm_o01():
    st.subheader("ORM^O01 - Order Message")
    pid = st.text_input("Patient ID")
    order_id = st.text_input("Order ID")
    test_ordered = st.text_input("Test Ordered")
    ordering_provider = st.text_input("Ordering Provider")
    clinical_instructions = st.text_area("Clinical Instructions")
    notes = st.text_area("Doctor Notes")
    return dict(pid=pid, order_id=order_id, test_ordered=test_ordered,
                ordering_provider=ordering_provider, clinical_instructions=clinical_instructions, notes=notes)

def input_oru_r01():
    st.subheader("ORU^R01 - Result Message")
    pid = st.text_input("Patient ID")
    observation_id = st.text_input("Observation ID")
    observation_value = st.text_input("Observation Value")
    units = st.text_input("Units")
    abnormal_flag = st.selectbox("Abnormal Flag", ["N", "H", "L", "A"])
    notes = st.text_area("Result Notes")
    return dict(pid=pid, observation_id=observation_id, observation_value=observation_value,
                units=units, abnormal_flag=abnormal_flag, notes=notes)

# Map message types & trigger events to input functions
input_map = {
    "ADT": {
        "A01": input_adt_a01,
        "A03": input_adt_a01,  # Reusing A01 for simplicity; can create separate functions if needed
        "A04": input_adt_a01,  # Reusing A01 for simplicity; can create separate functions if needed
        "A08": input_adt_a01,  # Reusing A01 for simplicity; can create separate functions if needed
        # Add others here...
    },
    "ORM": {
        "O01": input_orm_o01,
    },
    "ORU": {
        "R01": input_oru_r01,
    }
}

# Build PID segment from patient info
def build_pid(data):
    # Format: PID|||PatientID||LastName^FirstName||DOB|Gender|||
    name_parts = data['name'].split(" ", 1)
    last_name = name_parts[1] if len(name_parts) > 1 else ""
    first_name = name_parts[0]
    dob = hl7_date(data['dob'])
    gender = data.get('gender', 'O')
    return f"PID|||{data['pid']}||{last_name}^{first_name}||{dob}|{gender}|||"

# Build PV1 segment for ADT^A01 (admit)
def build_pv1(data):
    admit_date = hl7_date(data.get('admit_date', datetime.date.today()), include_time=True)
    location = data.get('location', 'ER')
    attending_doc = data.get('attending_doc', '1234^Doe^John')
    return f"PV1||I|{location}|||{attending_doc}|||||||||||{admit_date}"

# Build AL1 segment for allergies (one segment per allergy)
def build_al1(allergies_text):
    # Split allergies by lines or commas
    allergies = [a.strip() for a in allergies_text.split(",") if a.strip()]
    al1_segments = []
    for i, allergy in enumerate(allergies, start=1):
        # Simple fixed format: AL1|SetID|Type|Description
        al1_segments.append(f"AL1|{i}|DA|{allergy}")
    return al1_segments

# Build ORC segment for ORM^O01 (Order Control)
def build_orc(data):
    order_id = data['order_id']
    ordering_provider = data.get('ordering_provider', '1234^Smith^John')
    order_date = datetime.datetime.now().strftime("%Y%m%d%H%M")
    return f"ORC|NW|{order_id}|||" + f"|||" + f"|||{order_date}|||{ordering_provider}"

# Build OBR segment (Observation Request) for ORM^O01 or ORU^R01
def build_obr(data):
    obr_id = data.get('obr_id', '1')
    placer_order_num = data.get('placer_order_num', 'ORD123')
    filler_order_num = data.get('filler_order_num', 'FIL456')
    universal_service_id = data.get('universal_service_id', '88304^Pathology^L')
    order_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M")
    return f"OBR|{obr_id}|{placer_order_num}|{filler_order_num}|{universal_service_id}||||||||||||{order_datetime}||||||||"

# Build OBX segments for ORU^R01 observation results
def build_obx(obx_list):
    segments = []
    for obx in obx_list:
        segments.append(
            f"OBX|{obx['id']}|{obx['value_type']}|{obx['observation_id']}||"
            f"{obx['observation_value']}|{obx['units']}|{obx['reference_range']}|{obx['abnormal_flag']}|||F"
        )
    return segments

# Build NTE segments for notes (one segment per note)
def build_nte(notes_text):
    notes = [n.strip() for n in notes_text.split("\n") if n.strip()]
    nte_segments = []
    for i, note in enumerate(notes, start=1):
        nte_segments.append(f"NTE|{i}||{note}")
    return nte_segments


def main():
    st.set_page_config(page_title="EHR System", layout="centered")
    st.title("Modular EHR System - HL7 Message Builder")

    msg_event_map = {
        "ADT": ["A01", "A03", "A04", "A08"],
        "ORM": ["O01"],
        "ORU": ["R01", "R03"]
    }
    msg_type = st.selectbox("Message Type", list(msg_event_map.keys()))
    trigger_event = st.selectbox("Trigger Event", msg_event_map[msg_type])

    # Call the relevant input form function dynamically
    input_data = {}
    
    # ------- Logic # 1 -------
    # if msg_type in input_map and trigger_event in input_map[msg_type]:
    #     input_data = input_map[msg_type][trigger_event]()
    # else:
    #     st.warning("Input form not implemented for this message type and trigger event.")

    # if st.button("Build HL7 Message"):
    #     st.write("Building HL7 message with data:")
    #     st.json(input_data)
    #     # Here you would add your HL7 message builder logic based on input_data


    # ------- Logic # 2 -------
    # ADT^A01 inputs
    if msg_type == "ADT" and trigger_event == "A01":
        st.header("ADT^A01 - Admit Patient")

        input_data['pid'] = st.text_input("Patient ID", "12345")
        input_data['name'] = st.text_input("Patient Name (First Last)", "John Doe")
        input_data['dob'] = st.date_input("Date of Birth", datetime.date(1990, 1, 1))
        input_data['gender'] = st.selectbox("Gender", ["M", "F", "O"], index=2)
        input_data['admit_date'] = st.date_input("Admit Date", datetime.date.today())
        input_data['location'] = st.text_input("Admit Location", "ER")
        input_data['attending_doc'] = st.text_input("Attending Doctor (ID^Last^First)", "1234^Doe^John")
        allergies = st.text_area("Allergies (comma separated)", "Peanuts,Penicillin")
        notes = st.text_area("Nurse Notes")

    # ORM^O01 inputs
    elif msg_type == "ORM" and trigger_event == "O01":
        st.header("ORM^O01 - Order Message")

        input_data['pid'] = st.text_input("Patient ID", "12345")
        input_data['name'] = st.text_input("Patient Name (First Last)", "John Doe")
        input_data['dob'] = st.date_input("Date of Birth", datetime.date(1990, 1, 1))
        input_data['gender'] = st.selectbox("Gender", ["M", "F", "O"], index=2)
        input_data['order_id'] = st.text_input("Order ID", "ORD001")
        input_data['ordering_provider'] = st.text_input("Ordering Provider (ID^Last^First)", "1234^Smith^John")
        input_data['clinical_instructions'] = st.text_area("Clinical Instructions")
        notes = st.text_area("Doctor Notes")

    # ORU^R01 inputs
    elif msg_type == "ORU" and trigger_event == "R01":
        st.header("ORU^R01 - Observation Result")

        input_data['pid'] = st.text_input("Patient ID", "12345")
        input_data['name'] = st.text_input("Patient Name (First Last)", "John Doe")
        input_data['dob'] = st.date_input("Date of Birth", datetime.date(1990, 1, 1))
        input_data['gender'] = st.selectbox("Gender", ["M", "F", "O"], index=2)
        input_data['obr_id'] = st.text_input("OBR ID", "1")
        input_data['placer_order_num'] = st.text_input("Placer Order Number", "ORD123")
        input_data['filler_order_num'] = st.text_input("Filler Order Number", "FIL456")
        input_data['universal_service_id'] = st.text_input("Universal Service ID", "88304^Pathology^L")

        obx_list = []
        obx_count = st.number_input("Number of OBX segments", min_value=1, max_value=5, value=1, step=1)
        for i in range(obx_count):
            st.markdown(f"### OBX Segment {i+1}")
            obx = {
                'id': i+1,
                'value_type': st.selectbox(f"Value Type {i+1}", ["NM", "ST", "TX"], key=f"vt{i}"),
                'observation_id': st.text_input(f"Observation ID {i+1}", f"789{i}^TestCode{i}^L", key=f"obsid{i}"),
                'observation_value': st.text_input(f"Observation Value {i+1}", "100", key=f"obsval{i}"),
                'units': st.text_input(f"Units {i+1}", "mg/dL", key=f"units{i}"),
                'reference_range': st.text_input(f"Reference Range {i+1}", "80-120", key=f"ref{i}"),
                'abnormal_flag': st.text_input(f"Abnormal Flag {i+1}", "N", key=f"abn{i}"),
            }
            obx_list.append(obx)

        notes = st.text_area("Result Notes")

    else:
        st.warning("Input form not implemented for this message type and trigger event.")
        return

    if st.button("Build HL7 Message"):
        segments = [build_msh(msg_type, trigger_event), build_pid(input_data)]

        if msg_type == "ADT" and trigger_event == "A01":
            segments.append(build_pv1(input_data))
            segments.extend(build_al1(allergies))
            segments.extend(build_nte(notes))

        elif msg_type == "ORM" and trigger_event == "O01":
            segments.append(build_orc(input_data))
            segments.append(build_obr(input_data))
            segments.extend(build_nte(notes))

        elif msg_type == "ORU" and trigger_event == "R01":
            segments.append(build_obr(input_data))
            segments.extend(build_obx(obx_list))
            segments.extend(build_nte(notes))

        hl7_message = "\n".join(segments)
        st.code(hl7_message, language="hl7")

        # Send to receiver
        try:
            # response = requests.post("http://localhost:8000/ingest", data=hl7_message)

            response = requests.post(
                "http://localhost:8000/ingest",
                json={"message": hl7_message},
                timeout=10  # Optional: avoid indefinite hang
            )
            st.success("Message sent!")
            st.code(hl7_message, language="hl7")
            st.json(response.json())
        except Exception as e:
            st.error(f"Failed to send: {e}")


if __name__ == "__main__":
    main()



# """
# How to run:
# cd projects/Store_HL7/EHR_System
# streamlit run streamlit_EHR_app_v2.py
# """