string prompt = """
                Here is a transcript:
                {{TranscriptPlugin.Transcribe "https://assembly.ai/espn.m4a"}}
                ---
                Summarize the transcript.
                """;
var result = await kernel.InvokePromptAsync(prompt);
Console.WriteLine(result.GetValue<string>());
