interview_files = [os.path.join("interviews", file) for file in os.listdir("interviews")]

with open(output_filename, "w", newline="") as file:
    writer = csv.writer(file)
    header = ["Name", "Position", "Past Experience"]
    writer.writerow(header)

    print(f"Processing {len(interview_files)} interview files...")

    for interview_file in interview_files:
        print(f"\nProcessing: {interview_file}")

        # Upload file and get URL
        print("  Uploading file...")
        audio_url = upload_file(interview_file)

        # Transcribe audio
        print("  Transcribing...")
        transcript_text = transcribe_audio(audio_url)

        # Process with LLM Gateway
        print("  Analyzing with LLM Gateway...")
        llm_response = process_with_llm_gateway(transcript_text, prompt)

        # Parse JSON response
        interviewee_data = extract_json(llm_response)
        writer.writerow(interviewee_data.values())
        print(f"  Completed: {interviewee_data['Name']}")

print(f"\nCreated .csv file {output_filename}")
