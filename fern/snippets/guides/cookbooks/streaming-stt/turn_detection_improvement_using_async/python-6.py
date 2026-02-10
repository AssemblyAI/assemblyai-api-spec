def determine_streaming_config(aggregated_stats):
    if aggregated_stats is None:
        print("\nUsing default balanced configuration (no gap data available)")
        return {
            'name': 'Balanced (Default)',
            'end_of_turn_confidence_threshold': 0.4,
            'min_end_of_turn_silence_when_confident': 400,
            'max_turn_silence': 1280,
            'description': 'Standard configuration for general use'
        }

    print("\n" + "=" * 70)
    print("DETERMINING OPTIMAL STREAMING CONFIGURATION")
    print("=" * 70)

    avg_gap = aggregated_stats['overall_average_gap_ms']
    num_files = aggregated_stats['total_files_analyzed']

    print(f"\nBased on analysis of {num_files} file(s)")
    print(f"Overall average gap: {avg_gap:.0f} ms")

    # Determine configuration based on average gap
    if avg_gap < 500:
        config = {
            'name': 'Aggressive',
            'end_of_turn_confidence_threshold': 0.4,
            'min_end_of_turn_silence_when_confident': 160,
            'max_turn_silence': 400,
            'description': 'Fast-paced conversation with quick turn-taking'
        }
        use_cases = "IVR systems, order confirmations, yes/no queries, retail support"
    elif avg_gap < 1000:
        config = {
            'name': 'Balanced',
            'end_of_turn_confidence_threshold': 0.4,
            'min_end_of_turn_silence_when_confident': 400,
            'max_turn_silence': 1280,
            'description': 'Natural conversation pacing'
        }
        use_cases = "General customer support, consultations, standard voice agents"
    else:
        config = {
            'name': 'Conservative',
            'end_of_turn_confidence_threshold': 0.7,
            'min_end_of_turn_silence_when_confident': 800,
            'max_turn_silence': 3600,
            'description': 'Thoughtful, complex speech with longer pauses'
        }
        use_cases = "Technical support, healthcare, legal consultations, troubleshooting"

    print(f"\nSelected Configuration: {config['name']}")
    print(f"   Reasoning: Average gap of {avg_gap:.0f}ms indicates {config['description']}")
    print(f"\nConfiguration Parameters:")
    print(f"   • end_of_turn_confidence_threshold:        {config['end_of_turn_confidence_threshold']}")
    print(f"   • min_end_of_turn_silence_when_confident:  {config['min_end_of_turn_silence_when_confident']} ms")
    print(f"   • max_turn_silence:                        {config['max_turn_silence']} ms")
    print(f"\nRecommended use cases: {use_cases}")

    return config
