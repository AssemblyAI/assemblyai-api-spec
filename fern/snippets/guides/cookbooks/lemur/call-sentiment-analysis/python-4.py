answer_format = "<answer in one sentence> <reason in one sentence>"
questions = [
    {
        "question": "What was the overall sentiment of the call?",
        "context": customer_context,
        "answer_format": answer_format,
    },
    {
        "question": "What was the sentiment of the agent in this call?",
        "context": agent_context,
        "answer_format": answer_format,
    },
    {
        "question": "What was the sentiment of the customer in this call?",
        "context": customer_context,
        "answer_format": answer_format,
    },
    {
        "question": "What quote best demonstrates the customer's level of interest?",
        "context": customer_context,
        "answer_format": answer_format,
    },
    {
        "question": "Provide a quote from the agent that demonstrates their level of enthusiasm.",
        "context": agent_context,
        "answer_format": answer_format,
    },
]
