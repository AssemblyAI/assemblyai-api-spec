def on_close(ws, status, msg):
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print('\nDisconnected')

# Global audio resources (potential for memory leaks)
audio = pyaudio.PyAudio()
stream = audio.open(...)
