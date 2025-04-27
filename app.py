from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Transcript API is running!", 200

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({"error": "No videoId provided."}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript])
        return jsonify({"videoId": video_id, "transcript": transcript_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
