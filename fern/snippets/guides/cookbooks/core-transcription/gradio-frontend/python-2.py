import gradio

with gradio.Blocks() as demo:
    gradio.Markdown("# AssemblyAI Transcription with Gradio")
    filepath = gradio.File(file_types=["audio", "video"])
    transcribe_button = gradio.Button(value="Transcribe")
    transcript = gradio.Textbox(value="", label="Transcript")
    transcribe_button.click(transcribe, inputs=[filepath], outputs=[transcript])

if __name__ == "__main__":
    demo.launch(debug=True, show_error=True)
