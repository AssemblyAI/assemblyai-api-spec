# Send ForceEndpoint event to immediately end current turn
await websocket.send(json.dumps({
    "type": "ForceEndpoint"
}))
