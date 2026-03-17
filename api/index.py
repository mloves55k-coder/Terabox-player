from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api')
def extract():
    url = request.args.get('url')
    # Parrot backend jo aapne dhoonda
    api_url = f"https://tera.backend.live/api/get-info?url={url}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
        'Referer': 'https://terabox.com/'
    }
    try:
        r = requests.get(api_url, headers=headers, timeout=10)
        return jsonify(r.json())
    except:
        return jsonify({"error": "failed"}), 500
