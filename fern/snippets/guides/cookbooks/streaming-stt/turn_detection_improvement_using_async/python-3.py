def get_audio_files(folder_path):
    audio_extensions = {'.aac', '.ac3', '.aif', '.aiff', '.alac', '.amr', '.ape',
    '.au', '.dss', '.flac', '.m4a', '.m4b', '.m4p', '.mp3',
    '.mpga', '.ogg', '.oga', '.mogg', '.opus', '.qcp', '.tta',
    '.voc', '.wav', '.wv', '.webm', '.MTS', '.M2TS', '.TS',
    '.mov', '.mp4', '.m4v'}
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")

    audio_files = [
        str(f) for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in audio_extensions
    ]

    if not audio_files:
        raise ValueError(f"No audio files found in {folder_path}")

    return sorted(audio_files)
