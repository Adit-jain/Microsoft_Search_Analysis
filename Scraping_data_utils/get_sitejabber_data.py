from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL to scrape
base_url = "https://www.sitejabber.com/reviews/bing.com"
driver.get(base_url)
time.sleep(3)  # Wait for the page to load

reviews = []

while True:
    # Extract reviews
    review_elements = driver.find_elements(By.CSS_SELECTOR, "div.review-content")
    
    for review in review_elements:
        try:
            rating = review.find_element(By.CSS_SELECTOR, ".num").text.strip()
            text = review.find_element(By.CSS_SELECTOR, ".review-text").text.strip()
            date = review.find_element(By.CSS_SELECTOR, ".date").text.strip()
            reviews.append({"Rating": rating, "Review": text, "Date": date})
        except Exception as e:
            continue  # Skip if any field is missing

    # Try to click 'Next' button if available
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".pagination-next a")
        if "disabled" in next_button.get_attribute("class"):
            break  # Exit if no more pages
        next_button.click()
        time.sleep(3)  # Wait for next page to load
    except:
        break  # Exit if no next button found

driver.quit()

# Save to CSV
df = pd.DataFrame(reviews)
df.to_csv("bing_reviews.csv", index=False)
print("Scraping complete! Data saved as 'bing_reviews.csv'.")
