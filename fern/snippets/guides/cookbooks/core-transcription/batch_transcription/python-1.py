import assemblyai as aai
import threading
import os

aai.settings.api_key = "YOUR_API_KEY"
batch_folder = "audio"
transcription_result_folder = "transcripts"

transcriber = aai.Transcriber()

def transcribe_audio(audio_file):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(os.path.join(batch_folder, audio_file))
    if transcript.status == "completed":
        with open(f"{transcription_result_folder}/{audio_file}.txt", "w") as f:
            f.write(transcript.text)
    elif transcript.status == "error":
        print("Error: ", transcript.error)

threads = []
for filename in os.listdir(batch_folder):
    thread = threading.Thread(target=transcribe_audio, args=(filename,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All transcriptions are complete.")
