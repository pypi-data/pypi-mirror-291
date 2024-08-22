from mimic3_tts import Mimic3TextToSpeechSystem, Mimic3Settings
import os
import platform

def initialize_tts_system(voice_model='en_US/hifi-tts_low'):
    """Initialize the Mimic3 TTS system with the specified voice model."""
    settings = Mimic3Settings()
    settings.voice = voice_model
    return Mimic3TextToSpeechSystem(settings=settings)

def generate_audio(tts_system, text):
    """Generate audio data from the given text using the provided TTS system."""
    return tts_system.text_to_wav(text)

def save_audio(audio_data, filename="output.wav"):
    """Save the audio data to a specified file."""
    with open(filename, "wb") as f:
        f.write(audio_data)
    print(f"Audio file saved successfully as '{filename}'.")

def play_audio(filename="output.wav"):
    """Play the audio file using the appropriate command for the operating system."""
    if platform.system() == "Windows":
        os.system(f"start {filename}")
    elif platform.system() == "Darwin":  # macOS
        os.system(f"afplay {filename}")
    else:  # Linux
        os.system(f"aplay {filename}")

def hello_world():
    return print("Hello, world!")

def main():
    text = """
    Part three

    November 10–Present

    CHAPTER 14
    • Monday, November 10
    On Monday morning, Maxine is startled. The team has exceeded her expectations once again. They are all gathered in a conference room to quickly review status and talk about areas where they need help.
    “Before we start, there’s something I think we need to do,” Maggie says. “We really need a code name for this effort. If we’re working toward something big, we need to have a name. The more we accomplish, the more we’re going to have to talk about what we’re doing, and we can’t keep referring to ourselves as the Rebellion.”
    “What’s wrong with Promotions?” someone asks.
    “Well, that’s the name of the team,” she responds. “But the team has changed so much since our friends from Data Hub have joined, and there are so many new initiatives we’ve started. I think we need a new name because the way we’re working is so different than before.”
    """

    try:
        hello_world()
        # Step 1: Initialize the TTS system
        tts_system = initialize_tts_system()

        # Step 2: Generate audio from text
        audio_data = generate_audio(tts_system, text)

        # Step 3: Save the audio to a file
        save_audio(audio_data)

        # Step 4: Play the audio file
        play_audio()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
