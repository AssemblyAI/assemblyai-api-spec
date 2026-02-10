# Generate SRT content
sentences = transcript.get_sentences()
srt_content = process_segments(sentences)

# Save to SRT file
with open(filename + '.srt', 'w') as file:
    file.write(srt_content)

print(f"SRT file generated: {filename}.srt")
