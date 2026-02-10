def noise_reduced_mic_stream(sample_rate=16000):
    mic = aai.extras.MicrophoneStream(sample_rate=sample_rate)
    buffer = np.array([], dtype=np.int16)
    buffer_size = int(sample_rate * 0.5)  # 0.5 seconds
    for raw_audio in mic:
        audio_data = np.frombuffer(raw_audio, dtype=np.int16)
        buffer = np.append(buffer, audio_data)
        if len(buffer) >= buffer_size:
            float_audio = buffer.astype(np.float32) / 32768.0
            denoised = nr.reduce_noise(
                y=float_audio,
                sr=sample_rate,
                prop_decrease=0.75,
                n_fft=1024,
            )
            int_audio = (denoised * 32768.0).astype(np.int16)
            buffer = buffer[-1024:]  # keep some overlap
            yield int_audio.tobytes()
