def create_transcripts_embeddings(transcripts, granularity='paragraph'):
    # Dictionary to store embeddings with timestamps
    embeddings = {}
    total_tokens_embedded = 0

    for transcript in transcripts:
        if granularity == 'sentence':
            sentences = transcript.get_sentences()
            for sentence in sentences:
                # print(sentence.start, sentence.end)
                # print(sentence.text)
                total_tokens_embedded += num_tokens_from_string(sentence.text, 'r50k_base')

                embeddings[(sentence.start, transcript.id, sentence.text)] = embed_block(sentence.text)
        else:
            paragraphs = transcript.get_paragraphs()
            for paragraph in paragraphs:
                # print(paragraph.start, paragraph.end)
                # print(paragraph.text, '\n')
                total_tokens_embedded += num_tokens_from_string(paragraph.text, 'r50k_base')

                embeddings[(paragraph.start, transcript.id, paragraph.text)] = embed_block(paragraph.text)

    print(total_tokens_embedded, 'TOKENS EMBEDDED')
    print('COST OF EMBEDDINGS: $', (total_tokens_embedded / 1000)*0.0001)
    print()
    return embeddings
