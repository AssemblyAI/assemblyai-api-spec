def analyze_turn_detection(data):
    eot_confidence = data.get("end_of_turn_confidence", 0)

    if eot_confidence > 0.7:
        print("High confidence turn end - user definitely finished")
    elif eot_confidence > 0.4:
        print("Moderate confidence - may continue speaking")
    else:
        print("Low confidence - likely mid-sentence or thinking")
