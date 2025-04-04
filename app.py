import firebase_admin
from firebase_admin import credentials
import json
import streamlit as st
import random
from example import example
from trick import trick_1, trick_2, trick_3, trick_4
from firebase_admin import firestore
import streamlit.components.v1 as components
import datetime
import time



# Load Firebase secrets
# Load Firebase secrets
firebase_secrets = st.secrets["firebase"]

# Convert secrets to dict
cred_dict = {
    "type": firebase_secrets["type"],
    "project_id": firebase_secrets["project_id"],
    "private_key_id": firebase_secrets["private_key_id"],
    "private_key": firebase_secrets["private_key"].replace("\\n", "\n"),  # Fix multi-line key
    "client_email": firebase_secrets["client_email"],
    "client_id": firebase_secrets["client_id"],
    "auth_uri": firebase_secrets["auth_uri"],
    "token_uri": firebase_secrets["token_uri"],
    "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": firebase_secrets["client_x509_cert_url"],
    "universe_domain": firebase_secrets["universe_domain"],
}
cred = credentials.Certificate(json.loads(json.dumps(cred_dict)))
# Initialize Firebase (only if not already initialized)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Survey Pages Data (Replace with actual file names)
survey_data = [
    {"source_audio": "files/ssst/0011_000723.wav", "converted_audio": "files/ssst/0011_000023--0011_000723.wav"},
    {"source_audio": "files/ssst/0012_000725.wav", "converted_audio": "files/ssst/0012_000025--0012_000725.wav"},
    {"source_audio": "files/ssst/0013_000393.wav", "converted_audio": "files/ssst/0013_000043--0013_000393.wav"},
    {"source_audio": "files/ssst/0014_000379.wav", "converted_audio": "files/ssst/0014_000029--0014_000379.wav"},
    {"source_audio": "files/ssst/0015_001077.wav", "converted_audio": "files/ssst/0015_000027--0015_001077.wav"},
    {"source_audio": "files/ssst/0017_001076.wav", "converted_audio": "files/ssst/0017_000026--0017_001076.wav"},
    {"source_audio": "files/ssst/0018_001440.wav", "converted_audio": "files/ssst/0018_000040--0018_001440.wav"},
    {"source_audio": "files/ssst/0020_001436.wav", "converted_audio": "files/ssst/0020_000036--0020_001436.wav"},
    {"source_audio": "files/ssst/0020_001436.wav", "converted_audio": "files/ssst/0020_001436.wav"},
    {"source_audio": "files/ssdt/0011_000732.wav", "converted_audio": "files/ssdt/0011_000039--0011_000732.wav"},
    {"source_audio": "files/ssdt/0012_000385.wav", "converted_audio": "files/ssdt/0012_000028--0012_000385.wav"},
    {"source_audio": "files/ssdt/0013_001424.wav", "converted_audio": "files/ssdt/0013_000042--0013_001424.wav"},
    {"source_audio": "files/ssdt/0014_000380.wav", "converted_audio": "files/ssdt/0014_000031--0014_000380.wav"},
    {"source_audio": "files/ssdt/0015_001073.wav", "converted_audio": "files/ssdt/0015_000032--0015_001073.wav"},
    {"source_audio": "files/ssdt/0015_001079.wav", "converted_audio": "files/ssdt/0015_000032--0015_001079.wav"},
    {"source_audio": "files/ssdt/0016_001426.wav", "converted_audio": "files/ssdt/0016_000035--0016_001426.wav"},
    {"source_audio": "files/ssdt/0018_000730.wav", "converted_audio": "files/ssdt/0018_000025--0018_000730.wav"},
    {"source_audio": "files/ssst/0020_001436.wav", "converted_audio": "files/ssst/0020_000036.wav"},    
    {"source_audio": "files/dsst/0013_000723.wav", "converted_audio": "files/dsst/0011_000023--0013_000723.wav"},
    {"source_audio": "files/dsst/0018_000391.wav", "converted_audio": "files/dsst/0012_000041--0018_000391.wav"},
    {"source_audio": "files/dsst/0012_000394.wav", "converted_audio": "files/dsst/0013_000044--0012_000394.wav"},
    {"source_audio": "files/dsst/0012_000746.wav", "converted_audio": "files/dsst/0015_000046--0012_000746.wav"},
    {"source_audio": "files/dsst/0012_001425.wav", "converted_audio": "files/dsst/0016_000025--0012_001425.wav"},
    {"source_audio": "files/dsst/0015_001086.wav", "converted_audio": "files/dsst/0018_000036--0015_001086.wav"},
    {"source_audio": "files/dsst/0013_001438.wav", "converted_audio": "files/dsst/0019_000038--0013_001438.wav"},
    {"source_audio": "files/dsst/0019_001100.wav", "converted_audio": "files/dsst/0020_000050--0019_001100.wav"},
    {"source_audio": "files/ssst/0020_001436.wav", "converted_audio": "files/ssst/0020_000036.wav"},        
    {"source_audio": "files/dsdt/0012_000377.wav", "converted_audio": "files/dsdt/0011_000035--0012_000377.wav"},
    {"source_audio": "files/dsdt/0012_000380.wav", "converted_audio": "files/dsdt/0013_000040--0012_000380.wav"},
    {"source_audio": "files/dsdt/0011_000724.wav", "converted_audio": "files/dsdt/0014_000025--0011_000724.wav"},
    {"source_audio": "files/dsdt/0018_001442.wav", "converted_audio": "files/dsdt/0015_000032--0018_001442.wav"},
    {"source_audio": "files/dsdt/0015_001092.wav", "converted_audio": "files/dsdt/0016_000049--0015_001092.wav"},
    {"source_audio": "files/dsdt/0012_000737.wav", "converted_audio": "files/dsdt/0018_000044--0012_000737.wav"},
    {"source_audio": "files/dsdt/0016_001438.wav", "converted_audio": "files/dsdt/0019_000021--0016_001438.wav"},
    {"source_audio": "files/dsdt/0015_001080.wav", "converted_audio": "files/dsdt/0020_000041--0015_001080.wav"},
    {"source_audio": "files/ssst/0020_001436.wav", "converted_audio": "files/ssst/0020_001436.wav"},    
    {"source_audio": "files/uss/0011_000373.wav", "converted_audio": "files/uss/FSAH0_SI1874--0011_000373.wav"},
    {"source_audio": "files/uss/0015_000746.wav", "converted_audio": "files/uss/MKLS0_SA1--0015_000746.wav"},
    {"source_audio": "files/uss/0016_001089.wav", "converted_audio": "files/uss/MCPM0_SA2--0016_001089.wav"},
    {"source_audio": "files/uss/0018_001441.wav", "converted_audio": "files/uss/FSAH0_SX74--0018_001441.wav"},
    {"source_audio": "files/ssst/0020_001436.wav", "converted_audio": "files/ssst/0020_001436.wav"},    
    {"source_audio": "files/ute/1003_TIE_FEA_XX.wav", "converted_audio": "files/ute/0011_000021--1003_TIE_FEA_XX.wav"},
    {"source_audio": "files/ute/1043_TAI_DIS_XX.wav", "converted_audio": "files/ute/0015_000034--1043_TAI_DIS_XX.wav"},
    {"source_audio": "files/ute/1057_IWL_DIS_XX.wav", "converted_audio": "files/ute/0017_000038--1057_IWL_DIS_XX.wav"},
    {"source_audio": "files/ute/1089_IOM_FEA_XX.wav", "converted_audio": "files/ute/0016_000035--1089_IOM_FEA_XX.wav"},
    {"source_audio": "files/ssst/0020_001436.wav", "converted_audio": "files/ssst/0020_000036.wav"},
]

# Trick pages mapping
trick_pages = [trick_1, trick_2, trick_3, trick_4]

def survey_page(index):
    """Dynamically renders a survey page based on index"""
    if index < len(survey_data):
        st.markdown(
        '<p style="color:red; font-weight:bold;">'
        '**Reminder:** The content, speaker and duration may differ, but your rating should be based **only** on the speaking style and emotion.'
        '</p>', 
        unsafe_allow_html=True
        )
        source_audio = survey_data[index]["source_audio"]
        converted_audio = survey_data[index]["converted_audio"]

        # Extract only filenames, not full paths
        source_filename = source_audio.split("/")[-1]
        converted_filename = converted_audio.split("/")[-1]

        key = f"{source_filename} _ {converted_filename}"

        st.audio(source_audio, format="audio/wav", start_time=0)
        st.audio(converted_audio, format="audio/wav", start_time=0)

        rating = st.slider(f"Rate the emotional similarity (Page {index+1})", 1, 5, 3)
        
        return key, rating  # Return both key and rating
    return None, None

def submit_results(prolific_id, ratings):
    """Writes survey results to Firebase Firestore."""
    user_id = prolific_id if prolific_id else f"user_{int(time.time())}"  # Use Prolific ID if available
    timestamp = datetime.datetime.utcnow()

    # Prepare data to write
    data = {
        "prolific_id": prolific_id,
        "user_id": user_id,
        "timestamp": timestamp,
        "ratings": ratings
    }

    # Write to Firestore
    db.collection("survey_results").document(user_id).set(data)

def main():
    """Main function handling survey navigation and submission."""
    st.title("Survey Form for Emotional Speech Synthesis")

    session_state = st.session_state
    if "prolific_id" not in session_state:
        session_state["prolific_id"] = ""  # Store Prolific ID
    if "page" not in session_state:
        session_state["page"] = -1  # -1 for the Prolific ID input page
        session_state["ratings"] = {}
    if "completed" not in session_state:
        session_state["completed"] = False  # Flag to track completion

    total_pages = len(survey_data)

    if session_state["completed"]:
        # **Final Thank You Page**
        st.subheader("Thank You for Your Participation! 🎉")
        st.write("Your responses have been successfully submitted.")
        return  # Stop execution here

    if session_state["page"] == -1:
        # **Prolific ID Input Page**
        st.subheader("Enter Your Prolific ID")
        session_state["prolific_id"] = st.text_input("Prolific ID:", value=session_state["prolific_id"])
        
        if st.button("Next") and session_state["prolific_id"]:
            session_state["page"] = 0
            st.rerun()
        elif not session_state["prolific_id"]:
            st.warning("Please enter your Prolific ID to proceed.")

    elif session_state["page"] == 0:
        st.subheader("Example Page")
        st.write(
            "**Please note:** The content, duration and speaker may change between samples. "
            "Your task is to focus **only** on the speaking style and emotion."
        )
        example()
        if st.button("Next"):
            session_state["page"] = 1
            st.rerun()
    else:
        # **Survey Pages**
        page_index = session_state["page"] - 1

        if page_index < len(survey_data):
            key, rating = survey_page(page_index)

            if key and rating is not None:
                session_state["ratings"][key] = rating

        st.progress(session_state["page"] / total_pages)

        if session_state["page"] < total_pages:
            if st.button("Next"):
                session_state["page"] += 1
                st.rerun()
        else:
            st.subheader("Survey Completed! ✅")
            st.write("Please click 'Submit' to save your responses.")

            if st.button("Submit"):
                submit_results(session_state["prolific_id"], session_state["ratings"])
                session_state["completed"] = True  # Mark as completed
                st.rerun()  # Refresh to show Thank You page

if __name__ == "__main__":
    main()



