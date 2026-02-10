
from assemblyai_haystack.transcriber
from haystack.document_stores.in_memory
from haystack
from haystack.components.writers

ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")

document_store = InMemoryDocumentStore()
file_url = "https://assembly.ai/wildfires.mp3"

indexing = Pipeline()
indexing.add_component("transcriber", AssemblyAITranscriber(api_key=ASSEMBLYAI_API_KEY))
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("transcriber.transcription", "writer.documents")
indexing.run(
    {
        "transcriber": {
            "file_path": file_url,
            "summarization": None,
            "speaker_labels": None,
        }
    }
)

print("Indexed Document Count:", document_store.count_documents())
