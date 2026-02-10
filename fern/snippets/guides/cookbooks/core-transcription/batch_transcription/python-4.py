threads = []
for filename in os.listdir(batch_folder):
    thread = threading.Thread(target=transcribe_audio, args=(filename,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All transcriptions are complete.")
