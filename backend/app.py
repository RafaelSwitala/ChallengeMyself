from flask import Flask, request, jsonify
from flask_cors import CORS

from models.challenge import Challenge
from models.session import Session
from storage.json_storage import save_challenge, load_challenge
from models.activities import ACTIVITIES  

app = Flask(__name__)
CORS(app)  # erlaubt Requests vom React-Frontend

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/challenges", methods=["POST"])
def create_challenge():
    data = request.json
    name = data.get("name")

    if not name:
        return {"error": "name is required"}, 400

    if name not in ACTIVITIES:  # <--- Validierung hinzufügen
        return {"error": f"Unknown activity '{name}'"}, 400

    if load_challenge(name):
        return {"error": "challenge already exists"}, 400

    challenge = Challenge(name)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 201
    data = request.json
    name = data.get("name")

    if not name:
        return {"error": "name is required"}, 400

    if load_challenge(name):
        return {"error": "challenge already exists"}, 400

    challenge = Challenge(name)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 201

@app.route("/challenges/<name>/sessions", methods=["POST"])
def add_session(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    data = request.json
    date = data.get("date")
    values = data.get("values")

    if not date or not values:
        return {"error": "date and values required"}, 400

    session = Session(date, values)
    challenge.add_session(session)
    save_challenge(challenge)

    return jsonify(challenge.to_dict()), 200

@app.route("/challenges/<name>", methods=["GET"])
def get_challenge(name):
    challenge = load_challenge(name)
    if not challenge:
        return {"error": "challenge not found"}, 404

    return jsonify(challenge.to_dict())

if __name__ == "__main__":
    app.run(debug=True)
