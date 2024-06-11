from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    selected_categories = request.args.getlist('category')

    try:
        profile_response = requests.get('http://backend:5000/profiles')
        profile_response.raise_for_status()
        profiles = profile_response.json()
    except requests.exceptions.RequestException as e:
        profiles = []

    try:
        ad_links_response = requests.get('http://backend:5000/ad_links')
        ad_links_response.raise_for_status()
        ad_links = ad_links_response.json()
    except requests.exceptions.RequestException as e:
        ad_links = []

    if selected_categories:
        ad_links = [ad for ad in ad_links if ad['category'] in selected_categories]

    return render_template('index.html', profiles=profiles, ad_links=ad_links, selected_categories=selected_categories)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
