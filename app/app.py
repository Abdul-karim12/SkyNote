from flask import Flask, request, jsonify

app = Flask(__name__)

notes = []
note_id = 1

@app.route("/")
def home():
    return jsonify({"message": "SkyNote API is running"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)

@app.route("/notes", methods=["POST"])
def add_note():
    global note_id

    data = request.get_json()
    note = data.get("note")

    if not note:
        return jsonify({"error": "Note is required"}), 400

    new_note = {
        "id": note_id,
        "note": note
    }

    notes.append(new_note)
    note_id += 1

    return jsonify(new_note)

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    global notes

    notes = [note for note in notes if note["id"] != id]

    return jsonify({"message": f"Note {id} deleted"})
