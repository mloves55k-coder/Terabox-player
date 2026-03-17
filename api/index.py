from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/api')
def extract():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        # Hum aik naya stable API endpoint use karenge
        # Ye server TeraBox links ko direct stream mein convert karta hai
        api_endpoint = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={target_url}"
        
        response = requests.get(api_endpoint, timeout=10)
        data = response.json()
        
        # Alag alag API response formats handle karne ke liye
        video_url = ""
        if "stream_url" in data:
            video_url = data["stream_url"]
        elif "download_link" in data:
            video_url = data["download_link"]
        elif "list" in data and len(data["list"]) > 0:
            video_url = data["list"][0].get("main_url") or data["list"][0].get("direct_link")

        if video_url:
            return jsonify({"stream_url": video_url})
        else:
            return jsonify({"error": "Link not found in API response"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
