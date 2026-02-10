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
