def get_blackhole_device_index():
    """Find BlackHole audio device index."""
    p = pyaudio.PyAudio()
    blackhole_index = None

    print("Available audio devices:")

    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        print(f"  {i}: {dev_info['name']} (inputs: {dev_info['maxInputChannels']})")

        if str(dev_info['name']).startswith('BlackHole') and dev_info['maxInputChannels'] > 0:
            blackhole_index = i
            print(f"  -> Found BlackHole device at index {i}")

    p.terminate()
    return blackhole_index
