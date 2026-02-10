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
