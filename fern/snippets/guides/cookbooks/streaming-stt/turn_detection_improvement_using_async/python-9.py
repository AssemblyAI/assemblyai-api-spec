def main():
    try:
        # Step 1: Analyze all audio files in folder
        aggregated_stats = analyze_multiple_files(AUDIO_FOLDER_PATH, YOUR_API_KEY)

        # Step 2: Determine optimal configuration based on aggregated data
        streaming_config = determine_streaming_config(aggregated_stats)

        # Step 3: Run streaming with optimized settings
        run_streaming(streaming_config)

    except Exception as e:
        print(f"\nError in workflow: {str(e)}")
        raise

if __name__ == "__main__":
    main()
