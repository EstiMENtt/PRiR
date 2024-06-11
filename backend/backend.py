from flask import Flask, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB client setup
mongo_url = os.getenv('MONGO_URL', 'mongodb://mongo:27017')
client = MongoClient(mongo_url)
db = client['scraping_db']
profile_collection = db['profiles']
ad_links_collection = db['ad_links']

@app.route('/profiles', methods=['GET'])
def get_profiles():
    try:
        profiles = list(profile_collection.find({}, {'_id': False}))
        return jsonify(profiles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ad_links', methods=['GET'])
def get_ad_links():
    try:
        ad_links = list(ad_links_collection.find({}, {'_id': False}))
        return jsonify(ad_links)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
