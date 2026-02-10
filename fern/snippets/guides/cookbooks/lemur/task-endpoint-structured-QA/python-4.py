# -------------------------------
# Step 2: Build question helper functions
# -------------------------------
def construct_question(question):
    question_str = f"Question: {question['question']}"

    if question.get("context"):
        question_str += f"\nContext: {question['context']}"

    # Default answer_format
    if not question.get("answer_format"):
        question["answer_format"] = "short sentence"

    question_str += f"\nAnswer Format: {question['answer_format']}"

    if question.get("answer_options"):
        options_str = ", ".join(question["answer_options"])
        question_str += f"\nOptions: {options_str}"

    return question_str + "\n"

def escape_xml_characters(xml_string):
    return xml_string.replace("&", "&amp;")
