from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return jsonify({"message": "SkyNote API is running"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/notes", methods=["GET"])
def get_notes():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()

    return jsonify([dict(note) for note in notes])

@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    content = data.get("note")

    if not content:
        return jsonify({"error": "Note is required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": new_id, "note": content})

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Note {id} deleted"})








