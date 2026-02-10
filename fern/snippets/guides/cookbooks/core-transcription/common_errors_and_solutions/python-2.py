def filter_unsupported_characters(phrase):
    cleaned_phrase = `unicodedata.`normalize('NFKD', phrase).encode('ascii', 'ignore').decode('ascii')
    if len(cleaned_phrase) != len(phrase):
        raise Error("Unsupported characters in phrase")
    return cleaned_phrase
