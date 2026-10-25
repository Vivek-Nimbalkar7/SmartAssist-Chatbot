from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path
from chatbot import get_response

app = Flask(__name__)

# Create a folder for the database
DATABASE_DIR = Path("instance")
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE = DATABASE_DIR / "chatbot.db"


# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# Save conversations to the database
def save_chat(user_message, bot_response):
    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "INSERT INTO chat_logs (user_message, bot_response) VALUES (?, ?)",
        (user_message, bot_response)
    )

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400

    if len(user_message) > 1000:
        return jsonify({
            "response": "Please enter a message under 1000 characters."
        }), 400

    bot_response = get_response(user_message)

    save_chat(user_message, bot_response)

    return jsonify({"response": bot_response})


# Start the application
init_db()

if __name__ == "__main__":
    app.run(debug=True)