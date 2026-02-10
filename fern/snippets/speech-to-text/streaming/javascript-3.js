const token = await axios
  .post(
    "https://api.assemblyai.com/v2/realtime/token",
    { expires_in: 60 },
    {
      headers: {
        Authorization: "<apiKey>",
        "Content-Type": "application/json",
      },
    }
  )
  .then((response) => response.data.token);
