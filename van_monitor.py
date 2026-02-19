import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import requests
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("scraper_debug.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)

log.info("=== Van Scraper Started ===")

EMAIL = "oisinmcgrath1916@gmail.com"
PASS = "mateItisTimetoCrackaCookie2025^"

urls = [
    "https://www.facebook.com/marketplace/item/1991280048095762/",
    # Add your other URLs here
]

CSV_FILE = "Van_sales.csv"

# Persistent profile
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(r"user-data-dir=C:\Users\Oisin\ChromeProfile_VanScraper")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def login():
    log.info("Opening Facebook...")
    driver.get("https://www.facebook.com")
    time.sleep(5)

    # Force manual login if needed
    if "facebook.com/login" in driver.current_url or "checkpoint" in driver.current_url or "email" in driver.page_source.lower():
        log.info("Login page detected. Entering credentials...")
        try:
            driver.find_element(By.ID, "email").send_keys(EMAIL)
            driver.find_element(By.ID, "pass").send_keys(PASS)
            driver.find_element(By.NAME, "login").click()
            time.sleep(5)
        except:
            log.info("Credentials fields not found. Please enter manually.")
        input("Press ENTER after you have completed login/2FA and are on the home page...")

    else:
        log.info("Already logged in (persistent profile).")

login()

for url in urls:
    log.info(f"Processing: {url}")
    driver.get(url)
    time.sleep(6)

    # Scroll and click See more
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    try:
        see_more = driver.find_element(By.XPath, "//span[contains(text(), 'See more')]")
        see_more.click()
        time.sleep(2)
        log.info("Clicked 'See more'")
    except:
        pass

    row = {"Link": url, "Sold": "No"}

    try:
        title = driver.find_element(By.XPATH, "//h1//span").text.strip()
        row["Model"] = title.split(" - ")[0] if " - " in title else title
        log.info(f"Title: {title}")
    except:
        row["Model"] = "Unknown"

    try:
        price = driver.find_element(By.XPATH, "//span[contains(text(), '$')]").text.strip()
        row["Price"] = price
        log.info(f"Price: {price}")
    except:
        row["Price"] = "Unknown"

    desc = ""
    try:
        desc = driver.find_element(By.XPATH, "//div[@dir='auto' and contains(@class, 'x1iorvi4 x1pi30zi x1l90r2v x1swr2ck')]").text
    except:
        desc = driver.find_element(By.XPATH, "//div[@dir='auto']").text
    log.info(f"Description length: {len(desc)} characters")

    if desc and len(desc) > 20:
        prompt = f"""From this van description, extract:
- kms: current odometer (number only, highest relevant)
- transmission: A or M
- seller: seller name
Return ONLY valid JSON.

Text: {desc}"""

        try:
            r = requests.post("http://localhost:11434/api/generate", 
                              json={"model": "llama3.1:8b-instruct-q4_K_M", "prompt": prompt, "stream": False, "format": "json"})
            result = json.loads(r.json()["response"])
            row["Kms"] = result.get("kms", "Unknown")
            row["A/M"] = result.get("transmission", "Unknown")
            row["Seller"] = result.get("seller", "Unknown")
            log.info(f"Llama extracted → Kms: {row['Kms']} | A/M: {row['A/M']} | Seller: {row['Seller']}")
        except Exception as e:
            log.error(f"Llama failed: {e}")

    new_df = pd.DataFrame([row])
    if os.path.exists(CSV_FILE):
        existing = pd.read_csv(CSV_FILE)
        combined = pd.concat([existing, new_df], ignore_index=True)
        combined.to_csv(CSV_FILE, index=False)
    else:
        new_df.to_csv(CSV_FILE, index=False)

    log.info(f"Saved row for {url}")

driver.quit()
log.info("=== Scraper finished successfully ===")