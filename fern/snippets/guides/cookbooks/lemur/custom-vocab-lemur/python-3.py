from json import loads
from termcolor import colored

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
