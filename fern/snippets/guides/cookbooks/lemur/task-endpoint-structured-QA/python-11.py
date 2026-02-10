# -------------------------------
# Step 4: Build the LLM prompt
# -------------------------------
prompt = f"""You are an expert at giving accurate answers to questions about texts.
No preamble.
Given the series of questions, answer the questions.
Each question may follow up with answer format, answer options, and context for each question.
It is critical that you follow the answer format and answer options for each question.
When context is provided with a question, refer to it when answering the question.
You are useful, true and concise, and write in perfect English.
Only the question is allowed between the <question> tag. Do not include the answer format, options, or question context in your response.
Only text is allowed between the <question> and <answer> tags.
XML tags are not allowed between the <question> and <answer> tags.
End your response with a closing </responses> tag.
For each question-answer pair, format your response according to the template provided below:

Template for response:
<responses>
  <response>
    <question>The question</question>
    <answer>Your answer</answer>
  </response>
  <response>
    ...
  </response>
  ...
</responses>

These are the questions:
{question_str}

Transcript:
{transcript_text}
"""
