def get_duration_sox(file_path):
    command = ['soxi', '-D', file_path]
    try:
        duration = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(duration.stdout.strip())
    except ValueError:
        print("Error: Unable to parse duration from SoX output.")
        return None
