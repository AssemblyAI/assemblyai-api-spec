from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhooks/assemblyai", methods=["POST"])
def assemblyai_webhook():
    # Verify webhook authenticity
    if request.headers.get("X-Webhook-Secret") != "your_secret_here":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    transcript_id = data["transcript_id"]
    status = data["status"]

    if status == "completed":
        # Process completed transcript
        process_completed_meeting(data)
    elif status == "error":
        # Handle error
        log_transcription_error(transcript_id, data["error"])

    return jsonify({"received": True}), 200

def process_completed_meeting(transcript_data):
    """Process completed meeting transcript"""
    # Extract data
    utterances = transcript_data["utterances"]
    summary = transcript_data["summary"]

    # Store in database
    save_to_database(transcript_data)

    # Notify user
    send_notification(transcript_data["id"])
