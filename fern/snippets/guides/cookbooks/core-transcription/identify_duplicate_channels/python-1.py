from pydub import AudioSegment
import numpy as np

def load_audio(file_path):
    # Load the audio file.
    audio = AudioSegment.from_file(file_path)

    # Ensure audio is stereo.
    if audio.channels != 2:
        raise ValueError("This function only supports stereo audio files.")

    # Convert audio data to raw samples.
    samples = np.array(audio.get_array_of_samples())

    # Reshape samples to separate channels.
    samples = samples.reshape((-1, audio.channels))

    # Extract left and right channels.
    left_channel = samples[:, 0]
    right_channel = samples[:, 1]

    return left_channel, right_channel
