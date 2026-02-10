import assemblyai as aai

# SETTINGS
aai.settings.api_key = "YOUR-API-KEY"
filename = "YOUR-FILE-NAME"
transcriber = aai.Transcriber(config=aai.TranscriptionConfig(speaker_labels=True))
transcript = transcriber.transcribe(filename)

# Maximum number of words per subtitle
max_words_per_subtitle = 6

# Color assignments for speakers
speaker_colors = {
    "A": "red",
    "B": "orange",
    "C": "yellow",
    "D": "yellowgreen",
    "E": "green",
    "F": "lightskyblue",
    "G": "purple",
    "H": "mediumpurple",
    "I": "pink",
    "J": "brown",
}

# Process transcription segments
def process_segments(segments):
    srt_content = ""
    subtitle_index = 1
    for segment in segments:
        speaker = segment.speaker
        color = speaker_colors.get(speaker, "black")  # Default color is black

        # Split text into words and group into chunks
        words = segment.words
        for i in range(0, len(words), max_words_per_subtitle):
            chunk = words[i:i + max_words_per_subtitle]
            start_time = chunk[0].start  # -1 indicates continuation
            end_time = chunk[-1].end
            srt_content += create_subtitle(subtitle_index, start_time, end_time, chunk, color)
            subtitle_index += 1

    return srt_content


# Create a single subtitle
def create_subtitle(index, start_time, end_time, words, color):
    text = ""
    for word in words:
        text += word.text + ' '
    start_srt = format_time(start_time)
    end_srt = format_time(end_time)
    return f"{index}\n{start_srt} --> {end_srt}\n<font color=\"{color}\">{text}</font>\n\n"

# Format time in SRT style
def format_time(milliseconds):
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"

# Generate SRT content
sentences = transcript.get_sentences()
srt_content = process_segments(sentences)

# Save to SRT file
with open(filename + '.srt', 'w') as file:
    file.write(srt_content)

print(f"SRT file generated: {filename}.srt")
