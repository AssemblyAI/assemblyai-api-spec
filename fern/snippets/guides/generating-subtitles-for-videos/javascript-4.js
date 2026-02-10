async function getSubtitleFile(
  transcriptId: string,
  fileFormat: "srt"
): Promise<string> {
  if (!["srt", "vtt"].includes(fileFormat)) {
    throw new Error(
      `Unsupported file format: ${fileFormat}. Please specify 'srt' or 'vtt'.`
    );
  }

  const url = `https://api.assemblyai.com/v2/transcript/${transcriptId}/${fileFormat}`;

  try {
    const response = await axios.get<string>(url, { headers });
    return response.data;
  } catch (error: any) {
    throw new Error(
      `Failed to retrieve ${fileFormat.toUpperCase()} file: ${
        error.response?.status
      } ${error.response?.data?.error}`
    );
  }
}

const subtitles = await getSubtitleFile(
  transcriptId,
  "vtt" // or srt
);
await fs.writeFile("subtitles.vtt", subtitles);
console.log(subtitles);
