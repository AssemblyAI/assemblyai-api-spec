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
