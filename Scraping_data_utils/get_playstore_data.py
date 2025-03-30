from google_play_scraper import reviews_all, Sort
import pandas as pd

# App package name (Get it from the URL, e.g., https://play.google.com/store/apps/details?id=com.microsoft.bing)
app_package = ["com.microsoft.bingwebmastertools.twa", "com.microsoft.copilot", "com.microsoft.emmx", "com.microsoft.bing"]

# Scrape all reviews
for app in app_package:
    print(f"------------> {app}")
    reviews = reviews_all(
        app,
        lang="en",  # Language (change as needed)
        country="us",  # Country (change as needed)
        sort=Sort.MOST_RELEVANT  # 1 = Newest first, 2 = Highest rating, 3 = Lowest rating
    )

    # Convert to DataFrame
    df = pd.DataFrame(reviews)[["userName", "score", "at", "content"]]
    df.columns = ["User", "Rating", "Date", "Review"]

    # Save to CSV
    df.to_csv(f"google_play_reviews.{app}.csv", index=False)
    print(f"Scraping complete! Data saved as 'google_play_reviews.{app}.csv'.")
