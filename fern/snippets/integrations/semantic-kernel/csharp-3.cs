kernel.ImportPluginFromObject(
    new TranscriptPlugin(apiKey: apiKey)
    {
        AllowFileSystemAccess = true
    }
);
var result = await kernel.InvokeAsync(
    nameof(TranscriptPlugin),
    TranscriptPlugin.TranscribeFunctionName,
    new KernelArguments
    {
        ["INPUT"] = "https://assembly.ai/espn.m4a"
    }
);
Console.WriteLine(result.GetValue<string>());
