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
    celebrity_inspirations = request.args.get('celebs')  # comma-separated
    style_keywords = request.args.get('keywords')        # comma-separated

    celeb_list = celebrity_inspirations.split(',') if celebrity_inspirations else []
    keyword_list = style_keywords.split(',') if style_keywords else []

    query = generate_serpapi_query(celeb_list, keyword_list)
    print("[LOG] Optimized query generated:", query)

    params = {
        'engine': 'google_images',
        'q': query,
        'api_key': SERPAPI_API_KEY
    }

    serp_response = requests.get("https://serpapi.com/search", params=params).json()
    images = [img['original'] for img in serp_response.get('images_results', [])[:20]]

    print("[LOG] Returned images:", images)
    return jsonify({"images": images})

def generate_serpapi_query(celebrity_inspirations=None, style_keywords=None):
    query_parts = []

    if celebrity_inspirations:
        query_parts.append(" ".join(celebrity_inspirations))

    if style_keywords:
        query_parts.append(" ".join(style_keywords))

    # Generalized dynamic quality filtering, no forced style
    query_parts.append("high quality outfits natural lighting full body -collage -text -watermark -ads -campaign")

    return " ".join(query_parts).strip()


if __name__ == '__main__':
    print("[LOG] Starting Google Image Agent...")
    app.run(host='0.0.0.0', port=8000)
