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
        # TeraBox official app bypass link
        api_url = f"https://www.terabox.com/share/list?shorturl={url.split('/s/')[1]}&root=1"
        
        headers = {
            'User-Agent': 'TeraBox;10.5.2;Android;10;Redmi 13C',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        
        r = requests.get(api_url, headers=headers, timeout=15)
        data = r.json()
        
        # Agar list mil jaye toh video link dhoondna
        if "list" in data:
            # Ye link generate karne ke liye humein unka download link use karna hoga
            file_info = data["list"][0]
            dlink = file_info.get("dlink")
            if dlink:
                return jsonify({"stream_url": dlink})
        
        return jsonify({"error": "Bypass failed, trying backup..."}), 404
    except:
        return jsonify({"error": "Server error"}), 500
