import time
import pymongo
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://newuser:user123@cluster0.hswxa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URI)
db = client['twitter_scraper']
collection = db['trending_topics']

# ProxyMesh configuration
PROXY_LIST = [
    "http://username:password@proxymesh1.com:31280",
    "http://username:password@proxymesh2.com:31280",
    "http://username:password@proxymesh3.com:31280"
]

def get_random_proxy():
    return random.choice(PROXY_LIST)

def scrape_twitter():
    # Configure Selenium with proxy
    options = Options()
    proxy = get_random_proxy()
    options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(options=options)
    driver.get("https://x.com/")

    # Login to Twitter
    time.sleep(2)
    username = driver.find_element(By.NAME, "session[username_or_email]")
    password = driver.find_element(By.NAME, "session[password]")
    username.send_keys("your_username")
    password.send_keys("your_password")
    password.submit()

    time.sleep(5)  # Allow time for login

    # Fetch "What's Happening" trends
    trends = driver.find_elements(By.XPATH, '//section[contains(@aria-labelledby,"accessible-list")]//span')[:5]
    trend_names = [trend.text for trend in trends if trend.text]

    # Close the driver
    driver.quit()

    # Create a record
    record = {
        "unique_id": str(datetime.utcnow().timestamp()),
        "trends": trend_names,
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip_address": proxy
    }

    # Insert into MongoDB Atlas
    collection.insert_one(record)
    return record
