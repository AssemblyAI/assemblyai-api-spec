subs = generate_subtitles_by_word_count(transcript, 6)
with open(f"{transcript.id}.srt", 'w') as o:
    final = '\n'.join(subs)
    o.write(final)

print("SRT file generated.")
