import streamlit as st

def trick_1():
    ratings = {}
    audio_files = ["files/TIMIT/0018_001429.wav", "files/TIMIT/0018_001429.wav"]
    labels = ['Source', 'Converted']

    # Display audio files with labels
    for audio, label in zip(audio_files, labels):
        st.subheader(label)
        audio_file = open(audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    identifier = audio_files[0] + audio_files[1]

    st.subheader("Rate based on EMOTION SIMILARITY between Source and Converted speech")
    options1 = [None, '1', '2', '3', '4', '5']
    responseemo = st.radio("Choose one:", options1, index=0, key = identifier+"emo")

    ratings[identifier+"emo"] = responseemo

    return ratings

def trick_2():
    
    ratings = {}
    audio_files = ["files/TIMIT/0011_001083.wav", "files/TIMIT/0018_001429.wav"]
    labels = ['Source', 'Converted']

    # Display audio files with labels
    for audio, label in zip(audio_files, labels):
        st.subheader(label)
        audio_file = open(audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    identifier = audio_files[0] + audio_files[1]

    st.subheader("Rate based on EMOTION SIMILARITY between Source and Converted speech")
    options1 = [None, '1', '2', '3', '4', '5']
    responseemo = st.radio("Choose one:", options1, index=0, key = identifier+"emo")

    ratings[identifier+"emo"] = responseemo

    return ratings

def trick_3():
    
    ratings = {}
    audio_files = ["files/TIMIT/0011_001083.wav", "files/TIMIT/0011_001083.wav"]
    labels = ['Source', 'Converted']

    # Display audio files with labels
    for audio, label in zip(audio_files, labels):
        st.subheader(label)
        audio_file = open(audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    identifier = audio_files[0] + audio_files[1]

    st.subheader("Rate based on EMOTION SIMILARITY between Source and Converted speech")
    options1 = [None, '1', '2', '3', '4', '5']
    responseemo = st.radio("Choose one:", options1, index=0, key = identifier+"emo")

    ratings[identifier+"emo"] = responseemo

    return ratings

def trick_4():
    
    ratings = {}
    audio_files = ["files/TIMIT/FSAH0_SA1.wav", "files/TIMIT/FSAH0_SA1.wav"]
    labels = ['Source', 'Converted']

    # Display audio files with labels
    for audio, label in zip(audio_files, labels):
        st.subheader(label)
        audio_file = open(audio, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/wav')
    identifier = audio_files[0] + audio_files[1]

    st.subheader("Rate based on EMOTION SIMILARITY between Source and Converted speech")
    options1 = [None, '1', '2', '3', '4', '5']
    responseemo = st.radio("Choose one:", options1, index=0, key = identifier+"emo")

    ratings[identifier+"emo"] = responseemo

    return ratings
