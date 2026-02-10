const rt = client.realtime.transcriber({
  ...
})

rt.on('session_information', (info: SessionInformation) => console.log(info));
