from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/get_transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('videoId')
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        subprocess.run([
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--skip-download",
            "--convert-subs", "srt",
            "-o", "%(id)s",
            video_url
        ], check=True)

        transcript_file = f"{video_id}.en.srt"
        
        if not os.path.exists(transcript_file):
            return jsonify({"error": "Transcript file not found."}), 404

        with open(transcript_file, "r", encoding="utf-8") as file:
            transcript_text = file.read()

        os.remove(transcript_file)

        return jsonify({"videoId": video_id, "transcript": transcript_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
