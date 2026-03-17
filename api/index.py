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
        # Hum aik naya open-source bypasser use karenge jo filhal working hai
        api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.terabox.com/'
        }
        
        r = requests.get(api_url, headers=headers, timeout=15)
        data = r.json()
        
        # Check for multiple possible video link keys
        video_url = ""
        if "list" in data and len(data["list"]) > 0:
            video_url = data["list"][0].get("main_url") or data["list"][0].get("direct_link")
        
        if video_url:
            return jsonify({"stream_url": video_url})
        return jsonify({"error": "Encryption mismatch"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
