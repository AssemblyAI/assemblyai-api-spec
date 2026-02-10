import deepl

def translate(text):
    translator = deepl.Translator(DEEPL_API_TOKEN)
    result = translator.translate_text(text, target_lang="EN-US") # Note: DeepL requires more formal language code
    return result.text

# Example usage
for sent in transcript.get_sentences():
  translated_text = translate(sent.text)
  print("Text: {}".format(sent.text))
  print("Translation: {}".format(translated_text))
  print()
