from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

# Configuration (adjust as needed)
WEBDRIVER_PATH = "/path/to/chromedriver"  # Replace with your ChromeDriver path
BASE_URL = "https://www.sitejabber.com/reviews/bing.com"
SCROLL_PAUSE_TIME = 2
MAX_PAGES_TO_SCRAPE = 5  # Set a maximum number of pages to scrape (optional)

def scrape_sitejabber_reviews(base_url, max_pages=None):
    """Scrapes reviews from Sitejabber, handling scrolling and clicking the 'Next' button."""

    service = Service(executable_path=WEBDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=service, options=options)

    all_reviews = []
    page_number = 1

    try:
        driver.get(base_url)

        while True:  # Loop through the paginated sections

            print(f"Scraping section: {page_number}")

            # Scroll to load dynamic content *before* attempting to find reviews
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            

            # Get the page source
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'lxml')

            # Extract reviews from the current page
            review_elements = soup.find_all('div', class_='review')  # *REPLACE THIS WITH CORRECT SELECTOR*

            for review_element in review_elements:
                try:
                    author_element = review_element.find('span', class_='consumer-name')
                    author = author_element.text.strip() if author_element else "N/A"
                    content_element = review_element.find('div', class_='review-content')
                    content = content_element.text.strip() if content_element else "N/A"

                    rating_element = review_element.find('div', class_='rating-stars')
                    rating = rating_element['data-rating'] if rating_element else 'N/A'

                    date_element = review_element.find('span', class_='review-date')
                    date = date_element.text.strip() if date_element else "N/A"

                    all_reviews.append({'author': author, 'content': content, 'rating': rating, 'date': date})

                except Exception as e:
                    print(f"Error extracting data from a review: {e}")


            # Find and click the "Next" button.
            try:
                #Wait for the next button to be clickable.
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "next_page"))  # Replace with the actual selector
                )
                next_button.click()  # Click the button

            except Exception as e:
                print("Next button not found or not clickable.  Assuming end of reviews.")
                break #Assume this is the last page.

            page_number += 1
            if max_pages and page_number > max_pages:
                print(f"Reached maximum page limit ({max_pages}). Stopping.")
                break #Stop here

            time.sleep(SCROLL_PAUSE_TIME) #Wait before scrape next section
            print("Moving to the next section...")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

    finally:
        driver.quit()  # Close the browser window

    return all_reviews


if __name__ == "__main__":
    reviews = scrape_sitejabber_reviews(BASE_URL, max_pages=MAX_PAGES_TO_SCRAPE)  # Pass max_pages

    if reviews:
        print(f"Successfully scraped {len(reviews)} reviews.")
        import csv

        with open("bing_sitejabber_reviews_full.csv", 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['author', 'content', 'rating', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader() #Write header
            writer.writerows(reviews) # Write the reviews

        print("Reviews saved to bing_sitejabber_reviews_full.csv")
    else:
        print("No reviews found.")