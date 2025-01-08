from datetime import datetime
from flask import Flask, request, jsonify
import os
import pickle
import random


MODEL_LOCATION = os.getenv("MODEL_LOCATION", "/app/playlist-generator-model/data/playlists_rules.pkl")
DEFAULT_RECOMMENDATIONS = os.getenv("DEFAULT_RECOMMENDATIONS", ["iSpy (feat. Lil Yachty)", "Panda", "Chill Bill"])
MAX_RECOMMENDATIONS = int(os.getenv("MAX_RECOMMENDATIONS", 10))
API_VERSION = os.getenv("API_VERSION", "v1")


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


@app.route("/api/recommend", methods=["POST"])
def recommend_songs():
    songs = request.json.get("songs")

    if not songs:
        return jsonify({"error": "No songs provided"}), 400
    
    recommendation_model, model_last_update = get_model_data()

    recommendations = get_recommendations(songs, recommendation_model)
    if not recommendations or len(recommendations) == 0:
        recommendations = DEFAULT_RECOMMENDATIONS
    
    return jsonify({
        "songs": recommendations,
        "model_date": model_last_update,
        "version": API_VERSION,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=52055)
