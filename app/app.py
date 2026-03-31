
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets

app = Flask(__name__)

DB_PATH = "/data/notes.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()


init_db()


def get_token_from_header():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    return auth_header.split(" ", 1)[1]


def get_current_user():
    token = get_token_from_header()

    if not token:
        return None

    conn = get_db()
    session = conn.execute("""
        SELECT users.id, users.username
        FROM sessions
        JOIN users ON sessions.user_id = users.id
        WHERE sessions.token = ?
    """, (token,)).fetchone()
    conn.close()

    return session


@app.route("/")
def home():
    return jsonify({"message": "SkyNote API is running"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
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

        return jsonify({"message": "User registered successfully"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if not user or not check_password_hash(user["password"], password):
        conn.close()
        return jsonify({"error": "Invalid username or password"}), 401

    token = secrets.token_hex(32)

    conn.execute(
        "INSERT INTO sessions (user_id, token) VALUES (?, ?)",
        (user["id"], token)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Login successful",
        "token": token
    })


@app.route("/notes", methods=["GET"])
def get_notes():
    user = get_current_user()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    notes = conn.execute(
        "SELECT id, content FROM notes WHERE user_id = ?",
        (user["id"],)
    ).fetchall()
    conn.close()

    return jsonify([dict(note) for note in notes])


@app.route("/notes", methods=["POST"])
def add_note():
    user = get_current_user()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    content = data.get("note")

    if not content:
        return jsonify({"error": "Note is required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (user_id, content) VALUES (?, ?)",
        (user["id"], content)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": new_id,
        "note": content
    }), 201


@app.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    user = get_current_user()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    content = data.get("note")

    if not content:
        return jsonify({"error": "Note is required"}), 400

    conn = get_db()
    result = conn.execute(
        "UPDATE notes SET content = ? WHERE id = ? AND user_id = ?",
        (content, id, user["id"])
    )
    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({
        "message": f"Note {id} updated",
        "note": content
    })


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    user = get_current_user()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    result = conn.execute(
        "DELETE FROM notes WHERE id = ? AND user_id = ?",
        (id, user["id"])
    )
    conn.commit()
    conn.close()

    if result.rowcount == 0:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": f"Note {id} deleted"})
