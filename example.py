import streamlit as st

def example():
    st.markdown("<h2 style='color:red;'>We will first see an example.</h2>", unsafe_allow_html=True)  
    st.markdown("<br>", unsafe_allow_html=True)

    audio_files = ["examples/0014_000380_trg.wav", "examples/0011_0000210014_000380_diff.wav"]
    labels = ['Source', 'Converted']

    # Display audio files with labels
    for audio, label in zip(audio_files, labels):
        st.subheader(label)
        audio_file = open(audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    identifier = audio_files[0] + audio_files[1]

    st.subheader("Rate based on EMOTION SIMILARITY between Target and Converted speech")
    options1 = [None, '1', '2', '3', '4', '5']
    responseemo = st.radio("Choose one:", options1, index=5, key = identifier+"emo")
    st.write("Rating should be high (4-5) as we note an emotion similarity")

    audio_files = ["examples/0014_000380_trg.wav", "examples/0011_0000210014_000380_hifi.wav"]
    labels = ['Source', 'Converted']

    # Display audio files with labels
    for audio, label in zip(audio_files, labels):
        st.subheader(label)
        audio_file = open(audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    identifier = audio_files[0] + audio_files[1]

    st.subheader("Rate based on EMOTION SIMILARITY between Target and Converted speech")
    options1 = [None, '1', '2', '3', '4', '5']
    responseemo = st.radio("Choose one:", options1, index=3, key = identifier+"emo")
    st.write("Rating should be moderate (2-4) as we note an emotion pattern difference towards the end")