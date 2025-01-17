from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import os
import pickle
import random


MODEL_LOCATION = os.getenv("MODEL_LOCATION", "/app/data/playlists_rules.pkl")
DEFAULT_RECOMMENDATIONS = os.getenv("DEFAULT_RECOMMENDATIONS", ["iSpy (feat. Lil Yachty)", "Panda", "Chill Bill", "Life Is A Highway"])
MAX_RECOMMENDATIONS = int(os.getenv("MAX_RECOMMENDATIONS", 10))
API_VERSION = os.getenv("API_VERSION", "0.0")


def get_model_data() -> tuple[dict[str, set[str]], dict[str, str]]:
    with open(MODEL_LOCATION, "rb") as f:
        recommendation_model = pickle.load(f)
    
    return recommendation_model["rules"], recommendation_model["metadata"]


def get_recommendations(songs: list[str], recommendation_model: dict[str, set[str]]) -> list[str]:
    recommendations = set()

    for song in songs:
        recommendations.update(recommendation_model.get(song.lower(), set()))
    
    recommendations = list(recommendations)
    random.shuffle(recommendations)

    return recommendations[:MAX_RECOMMENDATIONS]


app = Flask(__name__)
CORS(app, origins=["*"])


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/all-musics", methods=["GET"])
def get_all_musics():
    recommendation_model, _ = get_model_data()

    return jsonify(list(recommendation_model.keys()))


@app.route("/api/recommend", methods=["POST"])
def recommend_songs():
    print("Received request to recommend songs")
    songs = request.json.get("songs")

    if not songs:
        return jsonify({"error": "No songs provided"}), 400
    
    try:
        recommendation_model, model_metadata = get_model_data()

        recommendations = get_recommendations(songs, recommendation_model)
        if not recommendations or len(recommendations) == 0:
            recommendations = DEFAULT_RECOMMENDATIONS
        
        return jsonify({
            "songs": recommendations,
            "model_date": model_metadata["last_update"],
            "version": API_VERSION,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Playlist Generator API...")
    app.run(host="0.0.0.0", port=52055)
