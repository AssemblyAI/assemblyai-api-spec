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

audio_file="./audio/8950.mp4"

if __name__ == "__main__":
    file_path = f"{audio_file}"
    main(file_path)
