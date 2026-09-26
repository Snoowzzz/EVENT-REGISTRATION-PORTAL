from flask import Flask, jsonify, abort, render_template

app = Flask(__name__)

EVENTS = [
    {
        "id": 1,
        "name": "Hackathon",
        "seats_total": 50,
        "seats_left": 50,
    },
    {
        "id": 2,
        "name": "AI Workshop",
        "seats_total": 30,
        "seats_left": 0,
    },
    {
        "id": 3,
        "name": "Cloud Computing Bootcamp",
        "seats_total": 40,
        "seats_left": 25,
    },
    {
        "id": 4,
        "name": "Startup Pitch Night",
        "seats_total": 20,
        "seats_left": 3,
    },
    {
        "id": 5,
        "name": "Web Dev Sprint",
        "seats_total": 35,
        "seats_left": 18,
    },
    {
        "id": 6,
        "name": "Cybersecurity CTF",
        "seats_total": 25,
        "seats_left": 0,
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.route("/api/events")
def get_events():
    return jsonify(EVENTS)


@app.route("/register/<int:event_id>", methods=["POST"])
def register(event_id):
    event = next((e for e in EVENTS if e["id"] == event_id), None)

    if event is None:
        abort(404, description="event not found")

    if event["seats_left"] <= 0:
        return {"error": "no seats left"}, 400

    event["seats_left"] -= 1
    return {"message": "registered", "seats_left": event["seats_left"]}, 200


if __name__ == "__main__":
    app.run(debug=True)
