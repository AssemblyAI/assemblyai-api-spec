const transcript = (
  await axios.get(
    "https://api.assemblyai.com/v2/transcript/YOUR_TRANSCRIPT_ID",
    { headers }
  )
).data;
