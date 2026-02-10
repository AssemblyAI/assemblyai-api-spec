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
