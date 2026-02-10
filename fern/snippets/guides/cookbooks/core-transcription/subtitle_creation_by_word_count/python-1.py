import assemblyai as aai

aai.settings.api_key = "YOUR-API-KEY"

transcriber = aai.Transcriber()

transcript = transcriber.transcribe("./my-audio.mp3")

def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)

    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

def generate_subtitles_by_word_count(transcript, words_per_line):
  output = []
  subtitle_index = 1  # Start subtitle index at 1
  word_count = 0
  current_words = []

  for sentence in transcript.get_sentences():
    for word in sentence.words:
      current_words.append(word)
      word_count += 1
      if word_count >= words_per_line or word == sentence.words[-1]:
        start_time = second_to_timecode(current_words[0].start / 1000)
        end_time = second_to_timecode(current_words[-1].end / 1000)
        subtitle_text = " ".join([word.text for word in current_words])
        output.append(str(subtitle_index))
        output.append("%s --> %s" % (start_time, end_time))
        output.append(subtitle_text)
        output.append("")
        current_words = []  # Reset for the next subtitle
        word_count = 0  # Reset word count
        subtitle_index += 1

  return output

subs = generate_subtitles_by_word_count(transcript, 6)
with open(f"{transcript.id}.srt", 'w') as o:
    final = '\n'.join(subs)
    o.write(final)

print("SRT file generated.")
