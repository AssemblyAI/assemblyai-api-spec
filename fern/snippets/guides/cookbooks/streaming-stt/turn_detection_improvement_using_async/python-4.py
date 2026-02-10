def analyze_single_file(audio_file, api_key, file_index, total_files):
    print("\n" + "=" * 70)
    print(f"ANALYZING FILE {file_index}/{total_files}: {Path(audio_file).name}")
    print("=" * 70)

    base_url = "https://api.assemblyai.com"
    headers = {"authorization": api_key}

    # Upload audio file
    print(f"\nUploading audio file...")

    if audio_file.startswith("http"):
        upload_url = audio_file
        print("Using provided URL")
    else:
        with open(audio_file, "rb") as f:
            response = requests.post(
                base_url + "/v2/upload",
                headers=headers,
                data=f
            )
        upload_url = response.json()["upload_url"]
        print(f"Upload complete")

    # Enable Speaker Labels
    data = {
        "audio_url": upload_url,
        "speaker_labels": True,
        # "language_detection": True # Enable automatic language detection if your files are in different languages
    }

    response = requests.post(
        base_url + "/v2/transcript",
        json=data,
        headers=headers
    )
    transcript_id = response.json()['id']
    print(f"Transcript ID: {transcript_id}")

    # Poll for completion
    print("\nWaiting for transcription to complete...")
    polling_endpoint = base_url + "/v2/transcript/" + transcript_id

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            print("Transcription completed!")
            break
        elif transcription_result['status'] == 'error':
            print(f"Transcription failed: {transcription_result['error']}")
            return None
        else:
            time.sleep(3)

    # Calculate gaps
    utterances = transcription_result['utterances']

    if len(utterances) < 2:
        print("⚠ Not enough utterances to analyze gaps (need at least 2)")
        return None

    gaps = []
    for i in range(len(utterances) - 1):
        current_end = utterances[i]['end']
        next_start = utterances[i + 1]['start']
        gap = next_start - current_end

        if gap > 0:
            gaps.append(gap)

    if not gaps:
        print("⚠ No gaps found between utterances (all speech overlaps)")
        return None

    # Calculate statistics
    stats = {
        'filename': Path(audio_file).name,
        'average_gap_ms': sum(gaps) / len(gaps),
        'min_gap_ms': min(gaps),
        'max_gap_ms': max(gaps),
        'median_gap_ms': sorted(gaps)[len(gaps) // 2],
        'total_utterances': len(utterances),
        'total_gaps': len(gaps),
        'all_gaps': gaps
    }

    print(f"\nResults for {stats['filename']}:")
    print(f"   Total utterances:  {stats['total_utterances']}")
    print(f"   Total gaps:        {stats['total_gaps']}")
    print(f"   Average gap:       {stats['average_gap_ms']:.0f} ms")
    print(f"   Median gap:        {stats['median_gap_ms']:.0f} ms")

    # Save transcript JSON to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = Path(audio_file).stem.replace(' ', '_')
    json_filename = f"transcript_{safe_filename}_{timestamp}.json"

    try:
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(transcription_result, f, indent=2, ensure_ascii=False)
        print(f"   Transcript saved:  {json_filename}")
    except Exception as e:
        print(f"   Error saving transcript: {e}")

    return stats
