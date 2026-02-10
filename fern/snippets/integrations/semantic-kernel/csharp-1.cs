using AssemblyAI.SemanticKernel;
using Microsoft.SemanticKernel;

// Build your kernel
var kernel = Kernel.CreateBuilder();

// Get AssemblyAI API key from env variables, or much better, from .NET configuration
string apiKey = Environment.GetEnvironmentVariable("ASSEMBLYAI_API_KEY")
  ?? throw new Exception("ASSEMBLYAI_API_KEY env variable not configured.");

kernel.ImportPluginFromObject(
    new TranscriptPlugin(apiKey: apiKey)
);
