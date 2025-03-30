import requests
from bs4 import BeautifulSoup
import time  # For rate limiting
import csv  # For saving to a CSV file
import json
import pandas as pd

def scrape_trustpilot_reviews(url, max_pages=10):
    """
    Scrapes reviews from a Trustpilot page with pagination, saving them to a CSV file.

    Args:
        url (str): The base URL of the Trustpilot review page (e.g., 'https://www.trustpilot.com/review/example.com').
        max_pages (int): The maximum number of pages to scrape.  Trustpilot might have many pages,
                       but you may want to limit this for testing/efficiency.
    """

    all_reviews = []

    for page_num in range(1, max_pages + 1):
        # Construct the URL for the current page
        if page_num == 1:
            page_url = url
        else:
            page_url = f"{url}?page={page_num}"  # Trustpilot usually uses ?page=N, check for your target URL
        print(f"Scraping page: {page_url}")

        try:
            response = requests.get(page_url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            soup = BeautifulSoup(response.content, 'html.parser')

            # --- ADJUST THIS SECTION BASED ON TRUSTPILOT'S HTML STRUCTURE ---
            # Find the elements containing the reviews. You'll need to inspect the page source.
            script_tags = soup.find_all('script', {'type': 'application/ld+json'})
            json_data = json.loads(script_tags[0].string)

            for data in json_data['@graph']:
                if data['@type'] == 'Review':
                    review = {
                        'author': data['author']['name'],
                        'date': data['datePublished'],
                        'review_body': data['reviewBody'],
                        'rating': data['reviewRating']['ratingValue']
                    }
                    all_reviews.append(review)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page_url}: {e}")
            break  # Stop if there's a network error

        except Exception as e:
            print(f"Error processing page {page_url}: {e}")  # General error handling
            break

        time.sleep(1)  # Rate limiting: Be respectful of the website

    # Save to CSV
    save_to_csv(all_reviews, "trustpilot_reviews.csv")
    print("Scraping completed.")

def save_to_csv(reviews, filename):
    """Saves the scraped reviews to a CSV file."""
    df = pd.DataFrame(reviews)
    df.to_csv(filename, index=False)


# Example Usage (Replace with the actual Trustpilot URL)
if __name__ == "__main__":
    trustpilot_url = "https://www.trustpilot.com/review/www.bing.com"  # ***REPLACE WITH THE ACTUAL URL***
    scrape_trustpilot_reviews(trustpilot_url, max_pages=1000)  #Scrape a maximum of 5 pages for testing