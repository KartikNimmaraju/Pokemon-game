from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import difflib
import requests

app = Flask(__name__)
CORS(app)

# List of all 150 Kanto Pokémon
kanto_pokemon = []
for i in range(1, 151):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
    kanto_pokemon.append({"name": response["name"].capitalize(), "image": response["sprites"]["front_default"]})

used_pokemon = []  # Track Pokémon already shown

# Serve a non-repeating Pokémon
@app.route("/pokemon", methods=["GET"])
def get_pokemon():
    global used_pokemon

    if len(used_pokemon) == len(kanto_pokemon):
        used_pokemon = []  
    remaining_pokemon = [p for p in kanto_pokemon if p not in used_pokemon]
    pokemon = random.choice(remaining_pokemon)
    used_pokemon.append(pokemon)

    return jsonify(pokemon)

# Check the user's guess (fuzzy matching)
@app.route("/guess", methods=["POST"])
def check_guess():
    data = request.json
    user_guess = data.get("guess", "").strip().lower()
    correct_name = data.get("correct_name", "").strip().lower()

    match = difflib.get_close_matches(user_guess, [correct_name], n=1, cutoff=0.75)

    if match:
        return jsonify({"correct": True})
    else:
        return jsonify({"correct": False})

if __name__ == "__main__":
    app.run(debug=True)
