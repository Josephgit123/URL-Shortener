import random
import string
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

# Initialize Database
conn = sqlite3.connect("urls.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, short TEXT, original TEXT)")
conn.commit()

def generate_short_code(length=6):
    """Generate a random short URL code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        original_url = request.form.get("url")

        # Generate unique short URL
        short_code = generate_short_code()
        cursor.execute("INSERT INTO urls (short, original) VALUES (?, ?)", (short_code, original_url))
        conn.commit()

        short_url = request.host_url + short_code  # Create full short URL
        return render_template("index.html", short_url=short_url)

    return render_template("index.html")

@app.route("/<short_code>")
def redirect_url(short_code):
    """Redirect short URL to the original URL."""
    cursor.execute("SELECT original FROM urls WHERE short=?", (short_code,))
    result = cursor.fetchone()
    if result:
        return redirect(result[0])
    return "URL not found!", 404

if __name__ == "__main__":
    app.run(debug=True)
