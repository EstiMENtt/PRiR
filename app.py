from flask import Flask, request, jsonify
from celery import Celery
import os

app = Flask(__name__)

# Konfiguracja Celery
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/start', methods=['POST'])
def start_scraping():
    try:
        app.logger.info("Received request: %s", request.data)
        data = request.json
        app.logger.info("Parsed JSON: %s", data)
        if not data:
            app.logger.error("Invalid JSON")
            return jsonify({"error": "Invalid JSON"}), 400
        task = scrape_data.apply_async(args=[data])
        app.logger.info("Task started: %s", task.id)
        return jsonify({"task_id": task.id}), 202
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@celery.task
def scrape_data(profile):
    # Składanie i przetwarzanie danych
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
