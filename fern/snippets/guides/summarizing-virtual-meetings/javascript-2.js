const path = "./my-audio.mp3";
const audioData = await fs.readFile(path);
const uploadResponse = await axios.post(`${baseUrl}/upload`, audioData, {
  headers,
});
const uploadUrl = uploadResponse.data.upload_url;
