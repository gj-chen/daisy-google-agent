from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    print("[LOG] Google Image Agent is running")
    return "Google Image Agent running!"

@app.route('/search-google-images', methods=['GET'])
def search_google_images():
    query = request.args.get('q')
    print("[LOG] Received query:", query)

    params = {
        'engine': 'google_images',
        'q': query,
        'api_key': SERPAPI_API_KEY
    }

    serp_response = requests.get("https://serpapi.com/search", params=params).json()
    print("[LOG] SerpAPI Response:", serp_response)

    images = [
        img['original']
        for img in serp_response.get('images_results', [])[:20]
    ]

    print("[LOG] Returned images:", images)
    return jsonify({"images": images})

if __name__ == '__main__':
    print("[LOG] Starting Google Image Agent...")
    app.run(host='0.0.0.0', port=8000)
