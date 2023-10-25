import streamlit as st
import speech_recognition as sr

def speech_recognition():
    """
    Function to create a Streamlit application for real-time speech recognition.

    This function uses the SpeechRecognition library to capture audio from the user's microphone
    and convert it to text using a speech recognition engine.

    The recognized text is displayed on the Streamlit application.

    Returns:
    - None
    """

    # Create a Streamlit application
    st.title("Real-time Speech Recognition")

    # Create a speech recognizer object
    recognizer = sr.Recognizer()

    # Create a microphone object
    microphone = sr.Microphone()

    # Start the microphone input
    with microphone as source:
        st.info("Listening...")

        # Adjust microphone energy threshold to ambient noise for better recognition
        recognizer.adjust_for_ambient_noise(source)

        # Continuously listen for audio and convert it to text
        while True:
            try:
                # Listen for audio input
                audio = recognizer.listen(source)

                # Recognize the audio and convert it to text
                text = recognizer.recognize_google(audio)

                # Display the recognized text on the Streamlit application
                st.write("You said:", text)

            except sr.UnknownValueError:
                # If the speech recognizer could not understand the audio
                st.warning("Could not understand audio")

            except sr.RequestError as e:
                # If there was an error with the speech recognition service
                st.error(f"Error: {e}")

speech_recognition()
