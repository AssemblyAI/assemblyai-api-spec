import { AssemblyAIClient, AssemblyAI } from "@assemblyai-fern/api";

const assemblyAI = new AssemblyAIClient({
  apiKey: "YOUR_API_KEY",
});

void main();

async function main() {
  const transcripts = await assemblyAI.transcript.list();
  console.log("Created application!", transcripts);
}
