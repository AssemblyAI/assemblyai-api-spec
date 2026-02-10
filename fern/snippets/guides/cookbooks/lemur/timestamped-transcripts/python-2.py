# Create prompt with timestamped utterances
prompt = f"""You are analyzing a transcript with timestamped utterances. Each utterance includes the text content, speaker label, and start/end timestamps in milliseconds.

Here is the transcript data:
{json.dumps(utterances_data, indent=2)}

Task: Identify the 3-5 most engaging, impactful, or quotable utterances from this transcript.

Return your response as a JSON array with the following structure:
{{
  "quotes": [
    {{
      "text": "exact quote text",
      "start": start_timestamp_in_milliseconds,
      "end": end_timestamp_in_milliseconds,
      "speaker": "speaker_label",
      "reason": "brief explanation of why this quote is engaging"
    }}
]
}}

Return ONLY valid JSON, no additional text."""

# Use LLM Gateway to extract quotes

print("Submitting transcript to LLM Gateway for quote extraction...")
gateway_response = requests.post(
"https://llm-gateway.assemblyai.com/v1/chat/completions",
headers=headers,
json={
"model": "gpt-5-nano",
"messages": [
{"role": "user", "content": prompt}
]
}
)

result = gateway_response.json()
quotes_json = json.loads(result["choices"][0]["message"]["content"])
print(json.dumps(quotes_json, indent=2))

````

</Tab>
<Tab title="JavaScript">
```javascript
// Create prompt with timestamped utterances
const prompt = `You are analyzing a transcript with timestamped utterances. Each utterance includes the text content, speaker label, and start/end timestamps in milliseconds.

Here is the transcript data:
${JSON.stringify(utterancesData, null, 2)}

Task: Identify the 3-5 most engaging, impactful, or quotable utterances from this transcript.

Return your response as a JSON array with the following structure:
{
  "quotes": [
    {
      "text": "exact quote text",
      "start": start_timestamp_in_milliseconds,
      "end": end_timestamp_in_milliseconds,
      "speaker": "speaker_label",
      "reason": "brief explanation of why this quote is engaging"
    }
  ]
}

Return ONLY valid JSON, no additional text.`;

// Use LLM Gateway to extract quotes
console.log("Submitting transcript to LLM Gateway for quote extraction...");
const gatewayResponse = await fetch(
  "https://llm-gateway.assemblyai.com/v1/chat/completions",
  {
    method: "POST",
    headers: headers,
    body: JSON.stringify({
      model: "gpt-5-nano",
      messages: [
        { role: "user", content: prompt }
      ]
    })
  }
);

const result = await gatewayResponse.json();
const quotesJson = JSON.parse(result.choices[0].message.content);
console.log(JSON.stringify(quotesJson, null, 2));
````

</Tab>
</Tabs>

## Example Response

```json
{
  "quotes": [
    {
      "text": "It is, it is. The levels outside right now in Baltimore are considered unhealthy. And most of that is due to what's called particulate matter, which are tiny particles, microscopic, smaller than the width of your hair, that can get into your lungs and impact your respiratory system, your cardiovascular system, and even your neurological, your brain.",
      "start": 62350,
      "end": 82590,
      "speaker": "B",
      "reason": "Defines particulate matter and explains how it harms health."
    },
    {
      "text": "Yeah. So the concentration of particulate matter, I was looking at some of the monitors that we have was reaching levels of what are, in science speak, 150 micrograms per meter cubed, which is more than 10 times what the annual average should be in about four times higher than what you're supposed to have on a 24 hour average. And so the concentrations of these particles in the air are just much, much, much higher than we typically see. And exposure to those high levels can lead to a host of health problems.",
      "start": 93550,
      "end": 123350,
      "speaker": "B",
      "reason": "Gives specific concentration figures and links to health risks."
    },
    {
      "text": "It's the youngest. So children, obviously, whose bodies are still developing, the elderly who are, you know, their bodies are more in decline and they're more susceptible to the health impacts of breathing, the poor air quality. And then people who have pre existing health conditions, people with respiratory conditions or heart conditions, can be triggered by high levels of air pollution.",
      "start": 137610,
      "end": 156650,
      "speaker": "B",
      "reason": "Highlights the most vulnerable groups affected by poor air quality."
    },
    {
      "text": "Well, I think the fires are going to burn for a little bit longer. But the key for us in the US Is the weather system changing. Right now it's the weather systems that are pulling that air into our Mid Atlantic and Northeast region. As those weather systems change and shift, we'll see that smoke going elsewhere and not impact us in this region as much. I think that's going to be the defining factor. I think the next couple days we're going to see a shift in that weather pattern and start to push the smoke away from where we are.",
      "start": 198280,
      "end": 227480,
      "speaker": "B",
      "reason": "Offers an outlook on how weather patterns may reduce exposure."
    },
    {
      "text": "I mean, that is one of the predictions for climate change. Looking into the future, the fire season is starting earlier and lasting longer and we're seeing more frequent fires. So yeah, this is probably something that we'll be seeing more, more frequently. This tends to be much more of an issue in the western U.S. so the eastern U.S. getting hit right now is a little bit new. But yeah, I think with climate change moving forward, this is something that is going to happen more frequently.",
      "start": 241370,
      "end": 267570,
      "speaker": "B",
      "reason": "Connects current event to longer-term climate change trends and future frequency."
    }
  ]
}
