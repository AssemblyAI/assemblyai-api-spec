import assemblyai as aai

aai.settings.api_key = "YOUR_API_KEY"
config = aai.TranscriptionConfig(speaker_labels=True)
transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3", config=config)

text = ""

for utt in transcript.utterances:
    text += f"Speaker {utt.speaker}:\n{utt.text}\n"

result = aai.Lemur().task(
    '''
    This is a speaker-labeled transcript of a podcast episode between Michel Martin, NPR host, and Peter DeCarlo, a professor at Johns Hopkins University.
    Please answer the following questions:
    1) Who is Speaker A and Speaker B?
    2) What questions did the podcast host ask?
    3) What were the main concerns of the podcast guest?"
    ''',
    input_text=text,
    final_model=aai.LemurModel.claude3_5_sonnet,
)

print(result.response)
