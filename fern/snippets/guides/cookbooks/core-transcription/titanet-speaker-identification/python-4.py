import requests
import os
from pydub import AudioSegment
import mimetypes
import wave


def download_and_convert_to_wav(url, output_dir="./content/converted_audio"):
    # Create the output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)

    # Extract filename from URL.
    filename = url.split("/")[-1].split("?")[0]
    base_filename, file_extension = os.path.splitext(filename)

    # Download the file.
    response = requests.get(url)
    if response.status_code == 200:
        # Determine the file type.
        content_type = response.headers.get("content-type")
        if content_type:
            guessed_extension = mimetypes.guess_extension(content_type)
            if guessed_extension:
                file_extension = guessed_extension

        # Save the downloaded file.
        downloaded_file = os.path.join(output_dir, filename)
        with open(downloaded_file, "wb") as f:
            f.write(response.content)

        # Generate the WAV file name.
        wav_filename = f"{base_filename}.wav"
        wav_file = os.path.join(output_dir, wav_filename)

        # Load the audio file.
        audio = AudioSegment.from_file(downloaded_file)

        # Convert to mono if it's stereo.
        if audio.channels > 1:
            print("Setting channels to 1.")
            audio = audio.set_channels(1)

        # Export as WAV.
        audio.export(wav_file, format="wav")
        print(f"File converted and saved as: {wav_file}")

        # Remove the original downloaded file if it's different from the WAV file.
        if downloaded_file != wav_file:
            os.remove(downloaded_file)

        # Ensure the WAV file is single channel.
        with wave.open(wav_file, "rb") as wf:
            n_channels = wf.getnchannels()
            if n_channels > 1:
                print(f"Converting {n_channels} channels to mono...")
                # Read the frames.
                frames = wf.readframes(wf.getnframes())
                # Get other parameters.
                params = wf.getparams()
                # Close the file.
                wf.close()
                # Convert to mono.
                mono_frames = b"".join([frames[i::n_channels] for i in range(n_channels)])
                # Write the mono WAV file.
                with wave.open(wav_file, "wb") as wf:
                    wf.setparams(
                        (1, params.sampwidth, params.framerate, params.nframes, params.comptype, params.compname)
                    )
                    wf.writeframes(mono_frames)
                print("Conversion to mono complete.")

        return wav_file
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return None
