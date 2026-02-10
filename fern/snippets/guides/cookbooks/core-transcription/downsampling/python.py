import subprocess

def convert_audio(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-ar', '16000',
        '-ac', '1',
        '-ab', '128k',
        output_file
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Conversion successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False

# Usage
convert_audio('input.wav', 'output.mp3')
