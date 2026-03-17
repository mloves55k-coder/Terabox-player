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
    
    # List of different bypassers to try
    endpoints = [
        f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={url}",
        f"https://terabox-api.p-v.workers.dev/api?url={url}"
    ]
    
    for api_url in endpoints:
        try:
            r = requests.get(api_url, timeout=10)
            if r.status_code == 200:
                res = r.json()
                # Try all possible keys for the video link
                stream = ""
                if "list" in res and res["list"]:
                    stream = res["list"][0].get("main_url") or res["list"][0].get("direct_link")
                elif "download_link" in res:
                    stream = res["download_link"]
                elif "url" in res:
                    stream = res["url"]
                
                if stream:
                    return jsonify({"stream_url": stream})
        except:
            continue
            
    return jsonify({"error": "Sare servers fail ho gaye. TeraBox ne ye link block kiya hai."}), 404
