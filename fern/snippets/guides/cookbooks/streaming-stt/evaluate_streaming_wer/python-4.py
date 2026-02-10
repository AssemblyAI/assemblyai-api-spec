# Initialize normalizers
normalizer = EnglishTextNormalizer()
# For Spanish and other languages
# normalizer = BasicTextNormalizer()

def calculate_wer(reference, hypothesis, language='en'):
    # Normalize both texts
    normalized_reference = normalizer(reference)
    print("Reference: " + reference)
    print("Normalized Reference: " + normalized_reference + "\n")

    normalized_hypothesis = normalizer(hypothesis)
    print("Hypothesis: " + hypothesis)
    print("Normalized Hypothesis: " + normalized_hypothesis+ "\n")

    # Calculate WER
    wer = jiwer.wer(normalized_reference, normalized_hypothesis)

    return wer * 100  # Return as percentage
