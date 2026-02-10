def analyze_multiple_files(folder_path, api_key):
    print("=" * 70)
    print("MULTI-FILE UTTERANCE GAP ANALYSIS")
    print("=" * 70)

    audio_files = get_audio_files(folder_path)
    total_files = len(audio_files)

    print(f"\nFound {total_files} audio file(s) in: {folder_path}")
    for i, file in enumerate(audio_files, 1):
        print(f"   {i}. {Path(file).name}")

    # Analyze each file
    all_file_stats = []
    all_gaps = []

    for i, audio_file in enumerate(audio_files, 1):
        try:
            stats = analyze_single_file(audio_file, api_key, i, total_files)
            if stats:
                all_file_stats.append(stats)
                all_gaps.extend(stats['all_gaps'])
        except Exception as e:
            print(f"\n✗ Error analyzing {Path(audio_file).name}: {str(e)}")
            continue

    if not all_file_stats:
        print("\n✗ No files were successfully analyzed")
        return None

    # Calculate aggregated statistics
    print("\n" + "=" * 70)
    print("AGGREGATED GAP ANALYSIS RESULTS")
    print("=" * 70)

    aggregated_stats = {
        'total_files_analyzed': len(all_file_stats),
        'total_utterances': sum(s['total_utterances'] for s in all_file_stats),
        'total_gaps': sum(s['total_gaps'] for s in all_file_stats),
        'overall_average_gap_ms': sum(all_gaps) / len(all_gaps),
        'overall_median_gap_ms': sorted(all_gaps)[len(all_gaps) // 2],
        'overall_min_gap_ms': min(all_gaps),
        'overall_max_gap_ms': max(all_gaps),
        'file_averages': [s['average_gap_ms'] for s in all_file_stats],
        'file_stats': all_file_stats
    }

    print(f"\nFiles successfully analyzed:  {aggregated_stats['total_files_analyzed']}/{total_files}")
    print(f"Total utterances (all files): {aggregated_stats['total_utterances']}")
    print(f"Total gaps analyzed:          {aggregated_stats['total_gaps']}")
    print(f"\nOverall average gap:          {aggregated_stats['overall_average_gap_ms']:.0f} ms ({aggregated_stats['overall_average_gap_ms']/1000:.2f} seconds)")
    print(f"Overall median gap:           {aggregated_stats['overall_median_gap_ms']:.0f} ms")
    print(f"Overall minimum gap:          {aggregated_stats['overall_min_gap_ms']:.0f} ms")
    print(f"Overall maximum gap:          {aggregated_stats['overall_max_gap_ms']:.0f} ms")

    # Show per-file breakdown
    print(f"\nPer-file average gaps:")
    for stat in all_file_stats:
        print(f"   • {stat['filename']:<40} {stat['average_gap_ms']:>6.0f} ms")

    # Calculate variability
    avg_of_file_averages = sum(aggregated_stats['file_averages']) / len(aggregated_stats['file_averages'])
    variability_ratio = aggregated_stats['overall_max_gap_ms'] / aggregated_stats['overall_average_gap_ms']

    print(f"\nAverage of file averages:     {avg_of_file_averages:.0f} ms")
    print(f"Variability ratio:            {variability_ratio:.2f}x")

    if variability_ratio > 3:
        print("└─> HIGH variability - mixed conversation patterns across files")
    elif variability_ratio > 2:
        print("└─> MODERATE variability - some pattern variation")
    else:
        print("└─> LOW variability - consistent conversation rhythm")

    # Save aggregated results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filename = f"aggregated_analysis_{timestamp}.json"

    try:
        summary_data = {
            'analysis_date': datetime.now().isoformat(),
            'folder_path': folder_path,
            'aggregated_statistics': {
                'total_files_analyzed': aggregated_stats['total_files_analyzed'],
                'total_utterances': aggregated_stats['total_utterances'],
                'total_gaps': aggregated_stats['total_gaps'],
                'overall_average_gap_ms': aggregated_stats['overall_average_gap_ms'],
                'overall_median_gap_ms': aggregated_stats['overall_median_gap_ms'],
                'overall_min_gap_ms': aggregated_stats['overall_min_gap_ms'],
                'overall_max_gap_ms': aggregated_stats['overall_max_gap_ms'],
                'variability_ratio': variability_ratio
            },
            'per_file_results': [
                {
                    'filename': s['filename'],
                    'average_gap_ms': s['average_gap_ms'],
                    'median_gap_ms': s['median_gap_ms'],
                    'total_utterances': s['total_utterances'],
                    'total_gaps': s['total_gaps']
                }
                for s in all_file_stats
            ]
        }

        with open(summary_filename, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        print(f"\nAggregated analysis saved to: {summary_filename}")
    except Exception as e:
        print(f"\nError saving aggregated analysis: {e}")

    return aggregated_stats
