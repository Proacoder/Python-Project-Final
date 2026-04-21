"""
chatbot/app.py  —  Flask backend for Gemini chatbot
Run:  python app.py
"""
from flask import Flask, request, jsonify, send_file, session
from flask_cors import CORS
import google.generativeai as genai
import os
import uuid
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILES = [Path(ROOT_DIR) / "api.env", Path(ROOT_DIR) / ".env"]

for env_file in ENV_FILES:
    if env_file.is_file():
        with env_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-this-in-production")
CORS(app)

# ── Gemini setup ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use gemini-2.5-flash as the latest available model
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None

# In-memory chat sessions keyed by session_id
# For production: replace with Redis or a database
chat_sessions: dict[str, object] = {}


def get_or_create_chat(session_id: str):
    """Return existing Gemini chat history or start a new one."""
    if session_id not in chat_sessions:
        chat_sessions[session_id] = model.start_chat(history=[])
    return chat_sessions[session_id]


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the chat UI."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return send_file(os.path.join(ROOT_DIR, "index.html"))


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    POST { "message": "...", "session_id": "..." }
    Returns { "reply": "...", "session_id": "..." }
    """
    data = request.get_json(force=True)
    user_message = (data.get("message") or "").strip()
    session_id   = data.get("session_id") or session.get("session_id") or str(uuid.uuid4())

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    if not GEMINI_API_KEY or not model:
        return jsonify({"error": "GEMINI_API_KEY not configured. Set it in your environment or api.env."}), 500

    try:
        chat_obj = get_or_create_chat(session_id)
        response = chat_obj.send_message(user_message)
        reply = response.text
    except Exception as e:
        return jsonify({"error": f"Gemini API error: {str(e)}"}), 500

    return jsonify({"reply": reply, "session_id": session_id})


@app.route("/api/reset", methods=["POST"])
def reset():
    """Clear the chat history for a session."""
    data       = request.get_json(force=True)
    session_id = data.get("session_id") or session.get("session_id")
    if session_id and session_id in chat_sessions:
        del chat_sessions[session_id]
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
