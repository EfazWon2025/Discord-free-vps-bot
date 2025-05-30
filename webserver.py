from flask import Flask
from threading import Thread
import logging

# Configure minimal logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def health_check():
    """Endpoint for health monitoring"""
    return {
        "status": "online",
        "service": "discord-vps-bot",
        "message": "VPS deployment bot is running"
    }, 200

@app.route('/ping')
def ping():
    """Liveness probe endpoint"""
    return "pong", 200

def run_webserver():
    """Start the Flask server in production mode"""
    from waitress import serve
    logger.info("Starting webserver on port 8080")
    serve(app, host="0.0.0.0", port=8080)

def keep_alive():
    """Start the webserver in a background thread"""
    server = Thread(target=run_webserver, daemon=True)
    server.start()
    logger.info("Webserver thread started")
