import assemblyai
from json import loads
from termcolor import colored

def correct_sentence(sentence, word_list = []):
    prompt = """
             You are an expert in correcting speech-to-text model outputs given a list of custom vocabulary words.
             You will be given a sentence from a transcript.
             You will also be given a list of custom vocabulary word that could be in the sentence.
             Your job is to identify any words from the custom vocabulary list that are in the sentence and correct them if they are spelled incorrectly.
             Only focus on spelling errors, you do not need to make corrections for miscased words.

             Only focus on corrections that are related to the custom vocabulary list.
             If there are no words from the custom vocabulary list in the sentence, you should return an empty array.
             If there are words from the list, return the original word, the corrected word, and your confidence in the correction.

             Return your answer in JSON with no explanation. The JSON should have the following format:
             [{
                 "original_word": "word1",
                 "corrected_word": "word2",
                 "confidence": 0.8
             }]
             """

    response = assemblyai.Lemur().task(
        prompt=prompt,
        input_text="Sentence: {}\nWord List: {}".format(sentence, ", ".join(word_list)),
        final_model=assemblyai.LemurModel.claude3_5_sonnet # Use .claude3_haiku for a faster, more cost-effective option.
    )

    return response.response

def correct_transcript(transcript, word_list = []):
    sentences = transcript.get_sentences()
    new_transcript = ""

    for sentence in sentences:

        # Optional: You can include word confidence scores as part of your input to guide LeMUR to incorrectly spelled words.
        # sentence_str = ""
        # for word in sentence.words:
        #     sentence_str += word.text + f" [{word.confidence}] "

        corrections = correct_sentence(sentence.text, word_list)
        corrections_json = loads(corrections)
        corrected_sentence = sentence.text

        for correction in corrections_json:
            if correction["confidence"] > 0.25: # Configure as needed.
                corrected_sentence = corrected_sentence.replace(correction["original_word"], correction["corrected_word"])
            else:
                print(colored("Confidence is less than 0.25", correction["original_word"], correction["corrected_word"], correction["confidence"], "red"))

        new_transcript += corrected_sentence + " "

        if len(corrections_json) > 0:
            print("Identified sentence to correct: ", colored(sentence.text, "yellow"))

    print()
    return new_transcript

assemblyai.settings.api_key = "YOUR_API_KEY"
transcriber = assemblyai.Transcriber()

transcript = transcriber.transcribe("https://drive.google.com/u/0/uc?id=1E1UUnabkXH-wN-CGbr-zd9dT_izZg1e6&export=download")

word_list = [
    'Azj-Kahet',
    'Neferess',
    "Ny'alotha",
    "Xal'atath"
    "Ansurek"
]

print(transcript.text)
print()
print(correct_transcript(transcript, word_list))
