import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/122.0.0.0 Safari/537.36"
}

@app.route('/search-google-images', methods=['GET'])
def search_google_images():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided."}), 400

    url = f"https://www.google.com/search?tbm=isch&q={query}"
    
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch images."}), 500

    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img')[1:21]  # Skip the first image (logo)

    image_urls = [img['src'] for img in images if 'src' in img.attrs]

    return jsonify({"images": image_urls})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8000)))