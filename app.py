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
np.random.shuffle(survey_data)
# Trick pages mapping
trick_pages = [trick_1, trick_2, trick_3, trick_4]

def survey_page(index):
    """Render a single survey page with audio and sliders. Saves ratings directly."""
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
                st.markdown(f"**Option {i + 1} ({method})**")
                try:
                    st.audio(audio_path, format="audio/wav")
                except Exception as e:
                    st.error(f"Error loading {method} audio: {audio_path}. Error: {e}")
                    st.error("Skipping rating for this option.")
                    continue

                source_filename = reference_audio_path.split(os.sep)[-1]
                converted_filename = audio_path.split(os.sep)[-1]
                rating_key = f"rating_{source_filename}_{converted_filename}_{method}"

                default_val = st.session_state.ratings.get(rating_key, 3)

                st.slider(
                    f"Similarity (Option {i+1} vs Reference)",
                    min_value=1, max_value=5, value=default_val,
                    key=rating_key
                )

        submit_clicked = st.form_submit_button("💾 Save Ratings for this Page")

    if submit_clicked:
        st.toast(f"Ratings for Task {index + 1} saved!", icon="✅")
        for i, (method, audio_path) in enumerate(method_items):
            if not audio_path:
                continue
            source_filename = os.path.basename(reference_audio_path)
            converted_filename = os.path.basename(audio_path)
            rating_key = f"rating_{source_filename}_{converted_filename}_{method}"

            if rating_key in st.session_state:
                st.session_state.ratings[rating_key] = st.session_state[rating_key]

        st.session_state["ratings_saved_for_index"] = index
        st.session_state["show_next_button"] = True







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

    # Use st.session_state directly for clarity
    if "prolific_id" not in st.session_state:
        st.session_state["prolific_id"] = ""
    if "page" not in st.session_state:
        # Page states: -1: ID, 0: Example, 1 to N: Survey pages, N+1: Submit page
        st.session_state["page"] = -1
        st.session_state["ratings"] = {} # Initialize central ratings dict
    if "completed" not in st.session_state:
        st.session_state["completed"] = False

    # Calculate total number of actual survey pages
    num_survey_pages = len(survey_data)
    # Total steps include ID (-1), Example (0), survey pages (1 to N)
    total_steps = num_survey_pages + 1

    # --- Final Thank You Page ---
    if st.session_state["completed"]:
        st.balloons()
        st.subheader("Thank You for Your Participation! 🎉")
        st.write("Your responses have been successfully submitted.")
        st.write("You may now close this window.")
        # Optionally display Prolific completion code here
        # st.code("YOUR_PROLIFIC_COMPLETION_CODE")
        return # Stop execution

    # --- Page Rendering Logic ---
    current_page = st.session_state["page"]

    if current_page == -1:
        # --- Prolific ID Input Page ---
        st.subheader("1. Enter Your Prolific ID")
        prolific_id_input = st.text_input("Prolific ID:", value=st.session_state["prolific_id"], key="prolific_id_widget")

        # Update session state if input changes
        st.session_state["prolific_id"] = prolific_id_input

        # Use columns for layout
        _, col2 = st.columns([3, 1]) # Push button to the right
        with col2:
            # Disable button if ID is empty
            proceed = st.button("Next Step ➡️", disabled=(not st.session_state["prolific_id"]))

        if proceed:
            st.session_state["page"] = 0 # Move to Example page
            st.rerun()
        # elif not st.session_state["prolific_id"] and st.button attempted: # Check if button was clicked without ID
        #      st.warning("Please enter your Prolific ID to proceed.")


    elif current_page == 0:
        # --- Example Page ---
        st.subheader("2. Example Task & Instructions")
        st.write(
            "**Instructions:** You will hear a reference audio sample followed by one or more converted audio samples. "
            "Please rate how similar the **speaking style and emotion** of each converted sample is to the reference sample on a scale of 1 (Not similar) to 5 (Very similar). "
        )
        st.warning(
            "**Important:** The verbal content, speaker identity, and duration might differ between the reference and converted samples. Please base your rating **only** on the similarity of the speaking style and emotion."
            )
        example() # Display the example content

        _, col2 = st.columns([3, 1])
        with col2:
            if st.button("Start Survey Tasks ➡️"):
                st.session_state["page"] = 1 # Move to first survey page
                st.rerun()

    elif 1 <= current_page <= num_survey_pages:
        # --- Survey Pages ---
        page_index = current_page - 1 # 0-based index for survey_data list

        # Display progress (adjusting for ID and Example pages)
        # Current step is 'page + 1' (since page starts at -1)
        # Total steps including ID, Example, N survey pages = N + 2
        progress_float = (current_page + 1) / (num_survey_pages + 2)
        st.progress(progress_float, text=f"Progress: Task {current_page} of {num_survey_pages}")

        # Render the survey page - it handles its own rating saving via its form
        survey_page(page_index)

        # --- Navigation Buttons (Below the Survey Page Form) ---
        st.divider()
        nav_cols = st.columns([1, 1, 1]) # Use 3 columns for Prev, Info, Next

        with nav_cols[2]:  # Next Button
            next_label = "Finish Survey Tasks ➡️" if current_page == num_survey_pages else "Next Task ➡️"
            if st.session_state.get("ratings_saved_for_index") == page_index:
                if st.button(next_label, key=f"next_btn_{page_index}"):
                    st.session_state.page += 1
                    st.session_state["show_next_button"] = False
                    st.rerun()
            else:
                st.button(next_label, disabled=True, key=f"next_btn_disabled_{page_index}")
                st.warning("Please save ratings for this page before proceeding.")

        with nav_cols[1]: # Page Indicator
             st.markdown(f"<div style='text-align: center;'>Task {current_page} / {num_survey_pages}</div>", unsafe_allow_html=True)


        with nav_cols[2]: # Next Button
             # Check if it's the last survey page
             next_label = "Finish Survey Tasks ➡️" if current_page == num_survey_pages else "Next Task ➡️"
             if st.button(next_label):
                 st.session_state.page += 1 # Move to next survey page or to submit page
                 st.rerun()

    elif current_page == num_survey_pages + 1:
        # --- Submission Page ---
        st.subheader(f"{num_survey_pages + 2}. Submit Your Responses")
        st.success("Survey tasks completed! ✅")
        st.write("Thank you for completing all the rating tasks. Please click 'Submit All Responses' below to finalize your participation.")
        st.warning("Ensure you have saved ratings on each page using the 'Save Ratings for this Page' button before submitting.")

        # Display collected ratings (optional, for user review)
        with st.expander("Review Your Ratings (Optional)"):
            st.json(st.session_state.ratings)

        _, col2 = st.columns([3, 1])
        with col2:
            if st.button("🚀 Submit All Responses"):
                submit_results(st.session_state["prolific_id"], st.session_state["ratings"])
                st.session_state["completed"] = True # Mark as completed
                st.rerun() # Refresh to show Thank You page

if __name__ == "__main__":
    main()



