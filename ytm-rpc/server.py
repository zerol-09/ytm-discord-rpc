from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

current_title = ""
current_artist = ""
current_thumbnail = ""
current_duration = 0
current_position = 0
current_playing = False
current_time = 0

@app.route("/song", methods=["POST"])
def song():
    global current_title
    global current_artist
    global current_thumbnail
    global current_duration
    global current_position
    global current_playing
    global current_time
    
    data = request.json
    current_title = data.get("title")
    current_artist = data.get("artist")
    current_thumbnail = data.get("thumbnail")
    current_duration = data.get("duration")
    current_position = data.get("position")
    current_playing = data.get("isPlaying")
    current_time = data.get("time")

    print("CURRENT TITLE:", current_title)
    print("CURRENT ARTIST:", current_artist)
    print("CURRENT THUMBNAIL:", current_thumbnail)
    print("CURRENT DURATION:", current_duration)
    print("CURRENT POSITION:", current_position)
    print("CURRENT PLAYING:", current_playing)
    print("CURRENT TIME:", current_time)
    print("="*20)
    return jsonify({"ok": True})

@app.route("/current")
def current():
    return jsonify({"title": current_title, "artist": current_artist, "thumbnail": current_thumbnail, "duration": current_duration, "position": current_position, "playing": current_playing, "time": current_time})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)