def check_audio_durations(file_path):
    #Check if audio durations differ among the three tools.
    ffprobe_duration = get_duration_ffprobe(file_path)
    sox_duration = get_duration_sox(file_path)
    mediainfo_duration = get_duration_mediainfo(file_path)

    # Print all retrieved durations
    print(f"ffprobe duration: {ffprobe_duration:.6f} seconds" if ffprobe_duration is not None else "ffprobe duration: Error retrieving duration")
    print(f"SoX duration: {sox_duration:.6f} seconds" if sox_duration is not None else "SoX duration: Error retrieving duration")
    print(f"MediaInfo duration: {mediainfo_duration:.6f} seconds" if mediainfo_duration is not None else "MediaInfo duration: Error retrieving duration")

    # Return durations for further checks
    return (ffprobe_duration, sox_duration, mediainfo_duration)
