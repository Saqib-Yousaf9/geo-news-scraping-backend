from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Railway!"

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Railway sets this PORT automatically
    app.run(host="0.0.0.0", port=port)
