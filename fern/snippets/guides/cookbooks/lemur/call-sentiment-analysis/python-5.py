# ------------------------------------------
# Step 4: Build prompt for the LLM
# ------------------------------------------
question_strs = []
for q in questions:
    q_str = f"Question: {q['question']}"
    if q.get("context"):
        q_str += f"\nContext: {q['context']}"
    if q.get("answer_format"):
        q_str += f"\nAnswer Format: {q['answer_format']}"
    question_strs.append(q_str)
questions_prompt = "\n\n".join(question_strs)
prompt = f"""
You are an expert at analyzing call transcripts.
Given the series of questions below, answer them accurately and concisely.
When context or answer format is provided, use it to guide your answers.
Transcript:
{transcript_text}
Questions:
{questions_prompt}
"""
