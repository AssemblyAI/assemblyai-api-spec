import assemblyai as aai

aai.settings.api_key = "API_KEY"

original_path = "FILE_PATH"

updated_path = convert_to_mono_if_duplicate(original_path)

# Check if we modified the file and thus appended _mono to it.
if updated_path != original_path:
    # Use the default configuration, which will treat the file as mono, which it now is.
    transcriber = aai.Transcriber()

    # Transcribe our new mono file.
    print(transcriber.transcribe(updated_path).text)
else:
    # Submit the file as Multi Channel if the content wasn't the same.
    config = aai.TranscriptionConfig(multichannel=True)

    # Load the config into our Transcriber.
    transcriber = aai.Transcriber(config=config)

    # Transcribe the stereo file.
    print(transcriber.transcribe(updated_path).text)
