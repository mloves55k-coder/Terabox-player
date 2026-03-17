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
        # Naya stable public bypasser
        api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        r = requests.get(api_url, headers=headers, timeout=15)
        res = r.json()
        
        # Multiple keys check karna kyunki formats badalte rehte hain
        stream = ""
        if "list" in res and res["list"]:
            item = res["list"][0]
            stream = item.get("main_url") or item.get("direct_link") or item.get("download_link")
        elif "download_link" in res:
            stream = res["download_link"]

        if stream:
            # Video player ko direct stream link bhejna
            return jsonify({"stream_url": stream})
        
        return jsonify({"error": "TeraBox ne encryption badal di hai"}), 404
    except Exception as e:
        return jsonify({"error": "Server error"}), 500
