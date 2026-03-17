from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/api')
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL"}), 400
    
    try:
        # Hum TeraBox ki aik alternative API use karte hain jo downloader sites use karti hain
        # Ye link ko direct handle karne ki koshish karega
        clean_url = url.split('?')[0]
        api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={clean_url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        
        r = requests.get(api_url, headers=headers, timeout=15)
        data = r.json()
        
        # Sabse stable link nikalne ki koshish
        video_link = ""
        if "list" in data and data["list"]:
            video_link = data["list"][0].get("main_url") or data["list"][0].get("direct_link")
        
        if video_link:
            return jsonify({"stream_url": video_link})
        
        return jsonify({"error": "TeraBox ne link hidden rakha hai. Koi doosra link try karein."}), 404
    except Exception as e:
        return jsonify({"error": "Extraction system busy"}), 500
