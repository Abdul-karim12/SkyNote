from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("/data/notes.db")
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
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

@app.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    data = request.get_json()
    content = data.get("note")

    if not content:
        return jsonify({"error": "Note is required"}), 400

    conn = get_db()
    conn.execute("UPDATE notes SET content = ? WHERE id = ?", (content, id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Note {id} updated", "note": content})

@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Note {id} deleted"})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User registered successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid username or password"}), 401
