const path = "./my-audio.mp3";
const audioData = await fs.readFile(path);
const urlResponse = await axios.post(`${baseUrl}/upload`, audioData, {
  headers,
});
const uploadUrl = urlResponse.data.upload_url;
