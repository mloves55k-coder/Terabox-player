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
        # Hum aik third-party bypasser use karenge jo zyada stable hai
        api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={url}"
        r = requests.get(api_url, timeout=10)
        res = r.json()
        
        # Check for multiple possible link locations
        stream = ""
        if "list" in res and res["list"]:
            stream = res["list"][0].get("main_url") or res["list"][0].get("direct_link")
        elif "download_link" in res:
            stream = res["download_link"]

        if stream:
            return jsonify({"stream_url": stream})
        return jsonify({"error": "Link not found"}), 404
    except:
        return jsonify({"error": "Extraction failed"}), 500
