import os

def convert_to_mono_if_duplicate(file_path):
    if compare_audio_channels(file_path):
        print("The audio content for this file is identical on both channels. Converting to mono...")

        # Load the audio file again with pydub.
        audio = AudioSegment.from_file(file_path)

        # Convert to mono by selecting one channel (since both are identical).
        mono_audio = audio.set_channels(1)

        # Save the new mono file.
        output_path = os.path.splitext(file_path)[0] + "_mono" + os.path.splitext(file_path)[1]
        mono_audio.export(output_path, format=os.path.splitext(file_path)[1][1:])

        print("File converted.\n")

        return output_path
    else:
        return file_path
