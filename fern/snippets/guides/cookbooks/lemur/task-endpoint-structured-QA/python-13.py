# -------------------------------
# Step 6: Parse and print XML response
# -------------------------------
clean_response = escape_xml_characters(llm_output).strip()

try:
    root = ET.fromstring(clean_response)
    for resp in root.findall("response"):
        question = resp.find("question").text
        answer = resp.find("answer").text
        print(f"Question: {question}")
        print(f"Answer: {answer}\n")
except ET.ParseError as e:
    print("Could not parse XML response.")
    print("Raw model output:\n", llm_output)
