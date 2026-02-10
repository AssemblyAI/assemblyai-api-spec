const audioData = await fs.readFile("./example.mp3");
const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, {
  headers,
});
const audioFile = uploadResponse.data.upload_url;
