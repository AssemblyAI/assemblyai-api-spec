import json, datetime

def get_citations(lemur_output):
    matches = find_relevant_matches(embeddings, lemur_output)

    print('CITATIONS:')
    for index, m in enumerate(matches):
        print('#{}'.format(index+1))
        print('QUOTE: "{}"'.format(m['text']))
        print('TRANSCRIPT ID:', m['transcript_id'])
        print('START TIMESTAMP:', str(datetime.timedelta(seconds=m['timestamp']/1000)))
        print('CONFIDENCE SCORE:', m['confidence'])
        print()
