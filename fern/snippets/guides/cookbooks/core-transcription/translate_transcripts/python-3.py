from translate import Translator

def translate(text):
    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    translation = translator.translate(text)
    return translation

for sent in transcript.get_sentences():
  translated_text = translate(sent.text)
  print("Text: {}".format(sent.text))
  print("Translation: {}".format(translated_text))
  print()
