from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_apscheduler import APScheduler
from pymongo import MongoClient
import time, io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt
import spacy
import subprocess
from datetime import datetime
import os
app = Flask(__name__)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

CORS(app)  # Allow all origins (or customize if needed)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

scheduler = APScheduler()
scheduler.init_app(app)


# Load NLP
#nlp = spacy.load("en_core_web_sm")

# MongoDB Setup
import os
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client['nap_db']
collection = db['nap_data']

def init_driver():
    options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
    options = webdriver.ChromeOptions()
 
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def test_selenium():
    driver = init_driver()
    driver.get("https://www.geo.tv/")
    print(driver.title)
    driver.quit()

@app.route('/test_selenium')
def test_selenium_route():
    test_selenium()
    return "Selenium Test Passed!"


# Scraping Job
def scrape_nap_data():
    driver = init_driver()
    driver.get("https://www.geo.tv/")
    time.sleep(3)

    article_links = driver.find_elements(By.CSS_SELECTOR, '.m_c_left ul li a.open-section')
    urls = list(set([link.get_attribute('href') for link in article_links]))

    collection.delete_many({})  # Clear old data

    for url in urls:
        driver.get(url)
        time.sleep(2)

        try:
            title = driver.find_element(By.TAG_NAME, 'h1').text
        except:
            title = ""

        try:
            name = driver.find_element(By.CSS_SELECTOR, 'div.author_title_img a').text
        except:
            name = "Web Desk"

        try:
            paragraphs = driver.find_elements(By.CSS_SELECTOR, 'div.content-area p')
            content = ' '.join([p.text for p in paragraphs])
        except:
            content = ""

        doc = nlp(content)
        persons = list(set([ent.text for ent in doc.ents if ent.label_ == "PERSON"]))[:3]
        possible_areas = ['Karachi', 'Lahore', 'Islamabad', 'Quetta', 'Peshawar', 'Sindh', 'Punjab', 'Balochistan', 'KPK']
        areas = [loc for loc in possible_areas if loc in content]

        collection.insert_one({
            'title': title,
            'name': name,
            'area': areas,
            'person': persons,
            'timestamp': datetime.utcnow()
        })

    driver.quit()
    print("Scraping complete and saved to MongoDB")

# Schedule every 30 mins
scheduler.add_job(id='Scrape Job', func=scrape_nap_data, trigger='interval', minutes=30)
scheduler.start()

@app.route('/')
def home():
    return "Welcome to the MongoDB NAP Scraper for Geo.tv"

@app.route('/get_nap')
def get_nap():
    data = list(collection.find({}, {'_id': 0}))
    return jsonify(data)

@app.route('/scrape_now')
def scrape_now():
    scrape_nap_data()
    return jsonify({"status": "Scraping completed successfully!"})

@app.route('/visualize_nap')
def visualize_nap():
    data = list(collection.find({}, {'_id': 0}))

    names = [item['name'] for item in data]
    areas = [area for item in data for area in item['area']]
    persons = [person for item in data for person in item['person']]

    name_counts = pd.Series(names).value_counts()
    area_counts = pd.Series(areas).value_counts()
    person_counts = pd.Series(persons).value_counts()

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    name_counts.plot(kind='bar', ax=axes[0], color='skyblue', title="Article Mentions by Author")
    axes[0].set_xlabel("Author")
    axes[0].set_ylabel("Count")

    area_counts.plot(kind='bar', ax=axes[1], color='salmon', title="Area Mentions")
    axes[1].set_xlabel("Area")
    axes[1].set_ylabel("Count")

    person_counts.plot(kind='bar', ax=axes[2], color='lightgreen', title="Person Mentions")
    axes[2].set_xlabel("Person")
    axes[2].set_ylabel("Count")

    img_io = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_io, format='png')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Railway sets this PORT automatically
    app.run(host="0.0.0.0", port=port)
