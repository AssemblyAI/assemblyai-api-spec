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
