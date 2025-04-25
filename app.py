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
import numpy as np


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
    {"reference": "samples_ZEST/ssst/0012_000725.wav", "zest": "samples_ZEST/ssst/0012_000025--0012_000725.wav", "gan": "samples_stargan/ssst/0012_000025--0012_000725.wav", "vevo": "samples_VEVO/ssst/0012_000025--0012_000725.wav"},
    {"reference": "samples_ZEST/ssst/0014_000379.wav", "zest": "samples_ZEST/ssst/0014_000029--0014_000379.wav", "gan": "samples_stargan/ssst/0014_000029--0014_000379.wav", "vevo": "samples_VEVO/ssst/0014_000029--0014_000379.wav"},
    {"reference": "samples_ZEST/ssst/0017_001076.wav", "zest": "samples_ZEST/ssst/0017_000026--0017_001076.wav", "gan": "samples_stargan/ssst/0017_000026--0017_001076.wav", "vevo": "samples_VEVO/ssst/0017_000026--0017_001076.wav"},
    {"reference": "samples_ZEST/ssst/0020_001436.wav", "zest": "samples_ZEST/ssst/0020_000036--0020_001436.wav", "gan": "samples_stargan/ssst/0020_000036--0020_001436.wav", "vevo": "samples_VEVO/ssst/0020_000036--0020_001436.wav"},
    {"reference": "samples_ZEST/dsst/0012_000394.wav", "zest": "samples_ZEST/dsst/0012_000394.wav", "gan": "samples_ZEST/dsst/0012_000394.wav", "vevo": "samples_ZEST/dsst/0012_000394.wav"},
    {"reference": "samples_ZEST/ssdt/0012_000385.wav", "zest": "samples_ZEST/ssdt/0012_000028--0012_000385.wav", "gan": "samples_stargan/ssdt/0012_000028--0012_000385.wav", "vevo": "samples_VEVO/ssdt/0012_000028--0012_000385.wav"},
    {"reference": "samples_ZEST/ssdt/0015_001073.wav", "zest": "samples_ZEST/ssdt/0015_000032--0015_001073.wav", "gan": "samples_stargan/ssdt/0015_000032--0015_001073.wav", "vevo": "samples_VEVO/ssdt/0015_000032--0015_001073.wav"},
    {"reference": "samples_ZEST/ssdt/0016_001426.wav", "zest": "samples_ZEST/ssdt/0016_000035--0016_001426.wav", "gan": "samples_stargan/ssdt/0016_000035--0016_001426.wav", "vevo": "samples_VEVO/ssdt/0016_000035--0016_001426.wav"},
    {"reference": "samples_ZEST/ssdt/0018_000730.wav", "zest": "samples_ZEST/ssdt/0018_000025--0018_000730.wav", "gan": "samples_stargan/ssdt/0018_000025--0018_000730.wav", "vevo": "samples_VEVO/ssdt/0018_000025--0018_000730.wav"},
    {"reference": "samples_ZEST/ute/1043_TAI_DIS_XX.wav", "zest": "samples_ZEST/ute/1043_TAI_DIS_XX.wav", "vevo": "samples_ZEST/ute/1043_TAI_DIS_XX.wav"},
    {"reference": "samples_ZEST/dsst/0013_000723.wav", "zest": "samples_ZEST/dsst/0011_000023--0013_000723.wav", "gan": "samples_stargan/dsst/0011_000023--0013_000723.wav", "vevo": "samples_VEVO/dsst/0011_000023--0013_000723.wav"},
    {"reference": "samples_ZEST/dsst/0012_000394.wav", "zest": "samples_ZEST/dsst/0013_000044--0012_000394.wav", "gan": "samples_stargan/dsst/0013_000044--0012_000394.wav", "vevo": "samples_VEVO/dsst/0013_000044--0012_000394.wav"},
    {"reference": "samples_ZEST/dsst/0012_001425.wav", "zest": "samples_ZEST/dsst/0016_000025--0012_001425.wav", "gan": "samples_stargan/dsst/0016_000025--0012_001425.wav", "vevo": "samples_VEVO/dsst/0016_000025--0012_001425.wav"},
    {"reference": "samples_ZEST/dsst/0015_001086.wav", "zest": "samples_ZEST/dsst/0018_000036--0015_001086.wav", "gan": "samples_stargan/dsst/0018_000036--0015_001086.wav", "vevo": "samples_VEVO/dsst/0018_000036--0015_001086.wav"},
    {"reference": "samples_ZEST/dsdt/0011_000724.wav", "zest": "samples_ZEST/dsdt/0011_000724.wav", "gan": "samples_ZEST/dsdt/0011_000724.wav", "vevo": "samples_ZEST/dsdt/0011_000724.wav"},
    {"reference": "samples_ZEST/dsdt/0012_000380.wav", "zest": "samples_ZEST/dsdt/0013_000040--0012_000380.wav", "gan": "samples_stargan/dsdt/0013_000040--0012_000380.wav", "vevo": "samples_VEVO/dsdt/0013_000040--0012_000380.wav"},
    {"reference": "samples_ZEST/dsdt/0011_000724.wav", "zest": "samples_ZEST/dsdt/0014_000025--0011_000724.wav", "gan": "samples_stargan/dsdt/0014_000025--0011_000724.wav", "vevo": "samples_VEVO/dsdt/0014_000025--0011_000724.wav"},
    {"reference": "samples_ZEST/dsdt/0016_001438.wav", "zest": "samples_ZEST/dsdt/0019_000021--0016_001438.wav", "gan": "samples_stargan/dsdt/0019_000021--0016_001438.wav", "vevo": "samples_VEVO/dsdt/0019_000021--0016_001438.wav"},
    {"reference": "samples_ZEST/dsdt/0015_001080.wav", "zest": "samples_ZEST/dsdt/0020_000041--0015_001080.wav", "gan": "samples_stargan/dsdt/0020_000041--0015_001080.wav", "vevo": "samples_VEVO/dsdt/0020_000041--0015_001080.wav"},
    {"reference": "samples_ZEST/ssst/0012_000725.wav", "zest": "samples_ZEST/ssst/0012_000725.wav", "gan": "samples_ZEST/ssst/0012_000725.wav", "vevo": "samples_ZEST/ssst/0012_000725.wav"},
    {"reference": "samples_ZEST/uss/0011_000373.wav", "zest": "samples_ZEST/uss/FSAH0_SI1874--0011_000373.wav", "gan": "samples_stargan/uss/FSAH0_SI1874--0011_000373.wav", "vevo": "samples_VEVO/uss/FSAH0_SI1874--0011_000373.wav"},
    {"reference": "samples_ZEST/uss/0015_000746.wav", "zest": "samples_ZEST/uss/MKLS0_SA1--0015_000746.wav", "gan": "samples_stargan/uss/MKLS0_SA1--0015_000746.wav", "vevo": "samples_VEVO/uss/MKLS0_SA1--0015_000746.wav"},
    {"reference": "samples_ZEST/uss/0016_001089.wav", "zest": "samples_ZEST/uss/MCPM0_SA2--0016_001089.wav", "gan": "samples_stargan/uss/MCPM0_SA2--0016_001089.wav", "vevo": "samples_VEVO/uss/MCPM0_SA2--0016_001089.wav"},
    {"reference": "samples_ZEST/uss/0018_001441.wav", "zest": "samples_ZEST/uss/FSAH0_SX74--0018_001441.wav", "gan": "samples_stargan/uss/FSAH0_SX74--0018_001441.wav", "vevo": "samples_VEVO/uss/FSAH0_SX74--0018_001441.wav"},
    {"reference": "samples_ZEST/ute/1089_IOM_FEA_XX.wav", "zest": "samples_ZEST/ute/1089_IOM_FEA_XX.wav", "vevo": "samples_ZEST/ute/1089_IOM_FEA_XX.wav"},
    {"reference": "samples_ZEST/ute/1003_TIE_FEA_XX.wav", "zest": "samples_ZEST/ute/0011_000021--1003_TIE_FEA_XX.wav", "vevo": "samples_VEVO/ute/0011_000021--1003_TIE_FEA_XX.wav"},
    {"reference": "samples_ZEST/ute/1043_TAI_DIS_XX.wav", "zest": "samples_ZEST/ute/0015_000034--1043_TAI_DIS_XX.wav", "vevo": "samples_VEVO/ute/0015_000034--1043_TAI_DIS_XX.wav"},
    {"reference": "samples_ZEST/ute/1057_IWL_DIS_XX.wav", "zest": "samples_ZEST/ute/0017_000038--1057_IWL_DIS_XX.wav", "vevo": "samples_VEVO/ute/0017_000038--1057_IWL_DIS_XX.wav"},
    {"reference": "samples_ZEST/ute/1089_IOM_FEA_XX.wav", "zest": "samples_ZEST/ute/0016_000035--1089_IOM_FEA_XX.wav", "vevo": "samples_VEVO/ute/0016_000035--1089_IOM_FEA_XX.wav"},
    ]
np.random.shuffle(survey_data)
# Trick pages mapping
trick_pages = [trick_1, trick_2, trick_3, trick_4]

def survey_page(index):
    """Render a single survey page with audio and sliders."""
    if index >= len(survey_data):
        return {}

    st.markdown(
        '<p style="color:red; font-weight:bold;">'
        '**Reminder:** The content, speaker and duration may differ, but your rating should be based **only** on the speaking style and emotion.'
        '</p>', 
        unsafe_allow_html=True
    )

    data = survey_data[index]
    reference_audio = data["reference"]
    method_audios = {
        "zest": data.get("zest"),
        "gan": data.get("gan"),
        "vevo": data.get("vevo")
    }
    method_audios = {k: v for k, v in method_audios.items() if v}

    st.subheader(f"Page {index + 1}")
    st.markdown("**Reference Audio**")
    st.audio(reference_audio, format="audio/wav")

    ratings = {}

    with st.form(key=f"form_page_{index}"):
        st.markdown("**Converted Audios**")
        cols = st.columns(len(method_audios))
        
        for i, (method, audio) in enumerate(method_audios.items()):
            with cols[i]:
                st.markdown(f"**Option {i + 1}**")
                st.audio(audio, format="audio/wav")

                source_filename = reference_audio.split("/")[-1]
                converted_filename = audio.split("/")[-1]
                rating_key = f"{source_filename}_{converted_filename}_{method}"

                # Use key to bind to session_state
                default_val = st.session_state.get(rating_key, 3)
                st.slider(
                    f"Similarity for Option {i + 1}",
                    min_value=1,
                    max_value=5,
                    value=default_val,
                    key=rating_key
                )

        # Submit button inside the form to save the ratings
        submit_clicked = st.form_submit_button("Save Ratings")

    # Store the ratings after form submission, but prevent page transition
    if submit_clicked:
        for method, audio in method_audios.items():
            source_filename = reference_audio.split("/")[-1]
            converted_filename = audio.split("/")[-1]
            rating_key = f"{source_filename}_{converted_filename}_{method}"
            ratings[rating_key] = st.session_state.get(rating_key, 3)

        # Update session_state with the saved ratings
        session_state = st.session_state
        if "ratings" not in session_state:
            session_state["ratings"] = {}

        for key, value in ratings.items():
            session_state["ratings"][key] = value

        # Keep the user on the current page, no automatic transition
        session_state["page"] = index  # Maintain the current page index

    return ratings




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
    db.collection("survey_results_comp").document(user_id).set(data)

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
            ratings = survey_page(page_index)

            # Save ratings only if not already stored to avoid overwriting unintentionally
            for key, val in ratings.items():
                if key not in session_state["ratings"]:
                    session_state["ratings"][key] = val

        st.progress(session_state["page"] / total_pages)

        # Ensure that moving to the next page only happens on explicit button press
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



