import requests

response = requests.post(
"https://aaigentsv1.up.railway.app/agents",
headers={
"Authorization": "YOUR_API_KEY",
"Content-Type": "application/json"
},
json={
"agent_name": "friendly_assistant",
"instructions": "You are a friendly and helpful assistant. Keep your responses concise and conversational. Be warm and personable.",
"voice": "luna",
"greeting": "Say hello and ask how you can help today."
}
)

print(response.json())

````
</Tab>
<Tab title="JavaScript">
```javascript
const response = await fetch("https://aaigentsv1.up.railway.app/agents", {
  method: "POST",
  headers: {
    "Authorization": "YOUR_API_KEY",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    agent_name: "friendly_assistant",
    instructions: "You are a friendly and helpful assistant. Keep your responses concise and conversational. Be warm and personable.",
    voice: "luna",
    greeting: "Say hello and ask how you can help today."
  })
});

console.log(await response.json());
````

</Tab>
</Tabs>

### Step 3: Start a conversation

Connect to your agent via WebSocket and start talking:
