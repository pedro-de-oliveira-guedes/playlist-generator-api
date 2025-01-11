from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import random


MODEL_LOCATION = os.getenv("MODEL_LOCATION", "/app/data/playlists_rules.pkl")
DEFAULT_RECOMMENDATIONS = os.getenv("DEFAULT_RECOMMENDATIONS", ["iSpy (feat. Lil Yachty)", "Panda", "Chill Bill", "Life Is A Highway"])
MAX_RECOMMENDATIONS = int(os.getenv("MAX_RECOMMENDATIONS", 10))
API_VERSION = os.getenv("API_VERSION", "0.0")


def get_model_data() -> tuple[dict[str, set[str]], str]:
    model_last_update = datetime.fromtimestamp(os.path.getmtime(MODEL_LOCATION)).strftime("%Y-%m-%d %H:%M:%S")

    with open(MODEL_LOCATION, "rb") as f:
        recommendation_model = pickle.load(f)
    
    return recommendation_model, model_last_update


def get_recommendations(songs: list[str], recommendation_model: dict[str, set[str]]) -> list[str]:
    recommendations = set()

    for song in songs:
        recommendations.update(recommendation_model.get(song.lower(), set()))
    
    recommendations = list(recommendations)
    random.shuffle(recommendations)

    return recommendations[:MAX_RECOMMENDATIONS]


app = Flask(__name__)
CORS(app, origins=["*"])


@app.route("/api/recommend", methods=["POST"])
def recommend_songs():
    print("Received request to recommend songs")
    songs = request.json.get("songs")

    if not songs:
        return jsonify({"error": "No songs provided"}), 400
    
    try:
        recommendation_model, model_last_update = get_model_data()

        recommendations = get_recommendations(songs, recommendation_model)
        if not recommendations or len(recommendations) == 0:
            recommendations = DEFAULT_RECOMMENDATIONS
        
        return jsonify({
            "songs": recommendations,
            "model_date": model_last_update,
            "version": API_VERSION,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Playlist Generator API...")
    app.run(host="0.0.0.0", port=7777)
