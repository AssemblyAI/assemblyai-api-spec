def compare_audio_channels(file_path):
    try:
        left_channel, right_channel = load_audio(file_path)

        # Compute hashes for both channels.
        left_hash = hash_audio_data(left_channel)
        right_hash = hash_audio_data(right_channel)

        # Compare hashes.
        if left_hash == right_hash:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
