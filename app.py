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
import os


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
# Trick pages mapping
trick_pages = [trick_1, trick_2, trick_3, trick_4]

def survey_page(index):
    """Render a single survey page with audio and sliders. Saves ratings and moves forward."""
    st.markdown(
        '<p style="color:red; font-weight:bold;">'
        '**Reminder:** The content, speaker and duration may differ, but your rating should be based **only** on the speaking style and emotion.'
        '</p>',
        unsafe_allow_html=True
    )

    data = survey_data[index]
    reference_audio_path = data["reference"]
    method_audio_paths = {
        "zest": data.get("zest"),
        "gan": data.get("gan"),
        "vevo": data.get("vevo")
    }
    method_audio_paths = {k: v for k, v in method_audio_paths.items() if v}

    st.subheader(f"Rating Task {index + 1} of {len(survey_data)}")
    st.markdown("**Reference Audio**")

    try:
        st.audio(reference_audio_path, format="audio/wav")
    except Exception as e:
        st.error(f"Error loading reference audio: {reference_audio_path}. Error: {e}")
        return

    with st.form(key=f"form_page_{index}"):
        st.markdown("**Converted Audios**")
        if not method_audio_paths:
            st.warning("No converted audio files found for this page.")
            cols = []
        else:
            cols = st.columns(len(method_audio_paths))

        method_items = list(method_audio_paths.items())
        for i, (method, audio_path) in enumerate(method_items):
            with cols[i]:
                st.markdown(f"**Option Heelo {i + 1}**")
                try:
                    st.audio(audio_path, format="audio/wav")
                except Exception as e:
                    st.error(f"Error loading {method} audio: {audio_path}. Error: {e}")
                    continue

                source_filename = os.path.basename(reference_audio_path)
                converted_filename = os.path.basename(audio_path)
                rating_key = f"rating_{source_filename}_{converted_filename}_{method}"
                default_val = st.session_state.ratings.get(rating_key, 3)

                st.slider(
                    f"Similarity (Option {i+1} vs Reference)",
                    min_value=1, max_value=5, value=default_val,
                    key=rating_key
                )

        # 🎯 THIS is now the only "next" button:
        submit_clicked = st.form_submit_button("✅ Save Ratings and Go to Next Page")

    if submit_clicked:
        for i, (method, audio_path) in enumerate(method_items):
            if not audio_path: continue
            source_filename = os.path.basename(reference_audio_path)
            converted_filename = os.path.basename(audio_path)
            rating_key = f"rating_{source_filename}_{converted_filename}_{method}"
            if rating_key in st.session_state:
                st.session_state.ratings[rating_key] = st.session_state[rating_key]
        st.toast(f"Ratings for Task {index + 1} saved!", icon="✅")
        st.session_state.page += 1
        st.rerun()


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
    st.title("Survey: Emotional Speech Style Similarity")

    if "prolific_id" not in st.session_state:
        st.session_state["prolific_id"] = ""
    if "page" not in st.session_state:
        st.session_state["page"] = -1
        st.session_state["ratings"] = {}
    if "completed" not in st.session_state:
        st.session_state["completed"] = False

    num_survey_pages = len(survey_data)

    if st.session_state["completed"]:
        st.balloons()
        st.subheader("Thank You for Your Participation! 🎉")
        st.write("Your responses have been successfully submitted.")
        return

    current_page = st.session_state["page"]

    if current_page == -1:
        st.subheader("1. Enter Your Prolific ID")
        prolific_id_input = st.text_input("Prolific ID:", value=st.session_state["prolific_id"], key="prolific_id_widget")
        st.session_state["prolific_id"] = prolific_id_input
        _, col2 = st.columns([3, 1])
        with col2:
            if st.button("Next Step ➡️", disabled=(not st.session_state["prolific_id"])):
                st.session_state["page"] = 0
                st.rerun()

    elif current_page == 0:
        st.subheader("2. Example Task & Instructions")
        st.write("**Instructions:** You will hear a reference audio sample followed by one or more converted audio samples. Please rate how similar the **speaking style and emotion** is.")
        st.warning("Content, speaker and duration might differ. Focus **only** on speaking style and emotion.")
        example()
        _, col2 = st.columns([3, 1])
        with col2:
            if st.button("Start Survey Tasks ➡️"):
                st.session_state["page"] = 1
                st.rerun()

    elif 1 <= current_page <= num_survey_pages:
        page_index = current_page - 1
        st.progress((current_page + 1) / (num_survey_pages + 2), text=f"Progress: Task {current_page} of {num_survey_pages}")
        survey_page(page_index)

        # ❌ No back/next buttons here — survey_page handles navigation

    elif current_page == num_survey_pages + 1:
        st.subheader(f"{num_survey_pages + 2}. Submit Your Responses")
        st.success("Survey tasks completed! ✅")
        st.write("Click 'Submit All Responses' below to finalize your participation.")
        st.warning("Make sure you clicked 'Save Ratings for this Page' on all tasks.")
        with st.expander("Review Your Ratings (Optional)"):
            st.json(st.session_state.ratings)

        _, col2 = st.columns([3, 1])
        with col2:
            if st.button("🚀 Submit All Responses"):
                submit_results(st.session_state["prolific_id"], st.session_state["ratings"])
                st.session_state["completed"] = True
                st.rerun()

if __name__ == "__main__":
    main()



