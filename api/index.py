from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api')
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL"}), 400
    
    try:
        # Parrot Downloader ka backend endpoint
        api_url = f"https://tera.backend.live/api/get-info?url={url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            'Origin': 'https://tera.backend.live',
            'Referer': 'https://tera.backend.live/'
        }
        
        r = requests.get(api_url, headers=headers, timeout=15)
        data = r.json()
        
        # Link nikalne ka logic
        stream_url = ""
        if "list" in data and len(data["list"]) > 0:
            stream_url = data["list"][0].get("main_url") or data["list"][0].get("direct_link")
        
        if stream_url:
            return jsonify({"stream_url": stream_url})
        else:
            return jsonify({"error": "Backend ne link nahi diya"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
