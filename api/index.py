from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/api')
def extract():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Parrot App ka actual API endpoint jo aapne PCAPdroid mein dekha
    api_url = "https://tera.backend.live/api/get-info"
    
    # Ye wo headers hain jo Parrot App bhejti hai taake block na ho
    headers = {
        'Host': 'tera.backend.live',
        'User-Agent': 'okhttp/4.9.3',
        'Content-Type': 'application/json; charset=utf-8',
        'Accept-Encoding': 'gzip'
    }

    # Parrot App ka secret JSON payload format
    payload = {
        "url": url,
        "token": "" # Baaz dafa ye empty bhi kaam karta hai
    }

    try:
        # Hum POST request bhejenge bilkul app ki tarah
        response = requests.post(api_url, headers=headers, json=payload, timeout=15)
        data = response.json()
        
        # Data extract karne ki koshish
        if "list" in data and len(data["list"]) > 0:
            stream_url = data["list"][0].get("main_url") or data["list"][0].get("direct_link")
            if stream_url:
                return jsonify({"stream_url": stream_url})
        
        return jsonify({"error": "Encryption layer 2 blocked us"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500
