import hashlib

def hash_audio_data(data):
    hasher = hashlib.sha256()
    hasher.update(data.tobytes())
    return hasher.hexdigest()
