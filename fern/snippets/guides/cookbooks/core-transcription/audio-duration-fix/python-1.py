import assemblyai as aai
import subprocess

aai.settings.api_key = "YOUR_API_KEY"
transcriber = aai.Transcriber()

def get_duration_ffprobe(file_path):
    command = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of',
        'default=noprint_wrappers=1:nokey=1', file_path
    ]
    try:
        duration = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(duration.stdout.strip())
    except ValueError:
        print("Error: Unable to parse duration from ffprobe output.")
        return None

def get_duration_sox(file_path):
    command = ['soxi', '-D', file_path]
    try:
        duration = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(duration.stdout.strip())
    except ValueError:
        print("Error: Unable to parse duration from SoX output.")
        return None

def get_duration_mediainfo(file_path):
    command = ['mediainfo', '--Output=General;%Duration%', file_path]
    try:
        duration_ms = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        duration_str = duration_ms.stdout.strip()
        # Check if the output is empty or not a valid number
        if duration_str:
            return float(duration_str) / 1000
        else:
            print("Error: MediaInfo returned empty or invalid duration")
            return None
    except ValueError:
        print("Error: Unable to parse duration from MediaInfo output.")
        return None

def check_audio_durations(file_path):
    #Check if audio durations differ among the three tools.
    ffprobe_duration = get_duration_ffprobe(file_path)
    sox_duration = get_duration_sox(file_path)
    mediainfo_duration = get_duration_mediainfo(file_path)

    # Print all retrieved durations
    print(f"ffprobe duration: {ffprobe_duration:.6f} seconds" if ffprobe_duration is not None else "ffprobe duration: Error retrieving duration")
    print(f"SoX duration: {sox_duration:.6f} seconds" if sox_duration is not None else "SoX duration: Error retrieving duration")
    print(f"MediaInfo duration: {mediainfo_duration:.6f} seconds" if mediainfo_duration is not None else "MediaInfo duration: Error retrieving duration")

    # Return durations for further checks
    return (ffprobe_duration, sox_duration, mediainfo_duration)

def transcribe(file):
    print("Executing transcription as audio durations are consistent.")
    transcript = transcriber.transcribe(file)
    print(transcript.text)

def transcode(input_file, output_file):
    #Transcode audio file to a 16kHz WAV file.
    print(f"Transcoding file {input_file} to {output_file}...")
    command = [
        'ffmpeg', '-i', input_file, '-ar', '16000', '-ac', '1', output_file
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if os.path.exists(output_file):
            print(f"Transcoding complete. Output file: {output_file}")
        else:
            print("Error: Transcoding failed.")
    except subprocess.CalledProcessError as e:
        print("Warnings from ffmpeg")
        """Print errors or warnings from ffmpeg"""
        #print(e.stderr.decode())

def durations_are_consistent(durations, tolerance=0.01):
    #Check if durations are consistent within a given tolerance of 0.01 seconds.
    if None in durations:
        return False
    min_duration = min(durations)
    max_duration = max(durations)
    return (max_duration - min_duration) <= tolerance

def main(file_path):
    durations = check_audio_durations(file_path)

    if durations:
        if None in durations:
            print("Error: One or more duration values could not be retrieved.")
            transcoded_file = file_path.rsplit('.', 1)[0] + '_transcoded.wav'
            transcode(file_path, transcoded_file)
            new_durations = check_audio_durations(transcoded_file)
            if new_durations and durations_are_consistent(new_durations):
                transcribe(transcoded_file)
            else:
                print("Warning: The audio durations still differ or an error occurred with the transcoded file.")
        elif not durations_are_consistent(durations):
            print("Warning: The audio durations differ between tools.")
            transcoded_file = file_path.rsplit('.', 1)[0] + '_transcoded.wav'
            transcode(file_path, transcoded_file)
            new_durations = check_audio_durations(transcoded_file)
            if new_durations and durations_are_consistent(new_durations):
                transcribe(transcoded_file)
            else:
                print("Warning: The audio durations still differ or an error occurred with the transcoded file.")
        else:
            print("The audio durations are consistent.")
            transcribe(file_path)

audio_file="./audio.mp4"

if __name__ == "__main__":
    file_path = f"{audio_file}"
    main(file_path)
