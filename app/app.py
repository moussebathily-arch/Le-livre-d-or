from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Connexion DB
conn = psycopg2.connect(
    host="db",
    database="guestbook",
    user="guest_user",
    password="guest_pass"
)
cur = conn.cursor()

# Login config
login_manager = LoginManager()
login_manager.init_app(app)

# ===== USER CLASS =====
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# ===== IA MODERATION =====
def is_clean(msg):
    banned = ["spam", "insulte", "hate"]
    return not any(word in msg.lower() for word in banned)

# ===== ROUTES =====

# Accueil
@app.route("/")
def home():
    return " Guestbook API running"

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Simple check (à remplacer par DB)
    if username == "admin" and password == "1234":
        user = User(1)
        login_user(user)
        return jsonify({"status": "logged in"})
    
    return jsonify({"error": "Invalid credentials"}), 401

# LOGOUT
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"status": "logged out"})

# AJOUT MESSAGE
@app.route("/add", methods=["POST"])
@login_required
def add_message():
    data = request.json
    name = data.get("name")
    message = data.get("message")

    if not is_clean(message):
        return jsonify({"error": "Message refusé "})

    cur.execute(
        "INSERT INTO messages (name, message) VALUES (%s, %s)",
        (name, message)
    )
    conn.commit()

    return jsonify({"status": "message ajouté"})

# GET MESSAGES
@app.route("/messages")
def get_messages():
    cur.execute("SELECT id, name, message FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    return jsonify(rows)

# LIKE MESSAGE
@app.route("/like/<int:id>", methods=["POST"])
@login_required
def like_message(id):
    cur.execute(
        "UPDATE messages SET likes = likes + 1 WHERE id = %s",
        (id,)
    )
    conn.commit()
    return jsonify({"status": "liked"})

# ADD COMMENT
@app.route("/comment", methods=["POST"])
@login_required
def add_comment():
    data = request.json
    message_id = data.get("message_id")
    content = data.get("content")

    cur.execute(
        "INSERT INTO comments (message_id, content) VALUES (%s, %s)",
        (message_id, content)
    )
    conn.commit()

    return jsonify({"status": "comment added"})

# GET COMMENTS
@app.route("/comments/<int:id>")
def get_comments(id):
    cur.execute(
        "SELECT content FROM comments WHERE message_id = %s",
        (id,)
    )
    rows = cur.fetchall()
    return jsonify(rows)

# Lancer serveur
app.run(host="0.0.0.0", port=5000)
