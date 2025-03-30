import praw
import pandas as pd
import time

# Reddit API credentials (replace these with your actual credentials)
REDDIT_CLIENT_ID = "XdyRG2biVhUD5eZiDfD0Jw"
REDDIT_CLIENT_SECRET = "GWUKpX-xZbmARKxfC4dAm4UpY-aZLA"
REDDIT_USER_AGENT = "windows:Redscrape:0.1 (by u/Own_Minimum7762)"

# Initialize PRAW
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

# List of keyword queries
queries = [
    "bing", "Bing Search", "Microsoft Bing", "Bing.com", "Bing vs Google", "Bing ranking", "Bing algorithm",
    "Bing AI", "Bing AI search", "AI-powered Bing", "Bing AI chatbot", "Bing Chat", "Bing ChatGPT", "Bing GPT",
    "Bing Copilot", "Microsoft Copilot", "Copilot AI", "Copilot pro", "Microsoft Copilot pro", "Copilot search",
    "Bing AI vs ChatGPT", "Bing AI vs Google Bard", "Bing AI vs Perplexity", "Bing AI vs Claude", "Bing vs DuckDuckGo",
    "Microsoft Search", "Windows Search", "Edge Bing Search", "Microsoft AI search", "Bing for Business",
    "Edge Bing Search", "Edge Copilot", "Microsoft Edge AI", "Edge search AI", "Edge browser AI", "Bing AI in Edge",
    "Bing AI Office 365", "Bing AI Teams", "Bing AI Excel", "Bing AI Word",
    "Bing AI features", "Bing AI accuracy", "Bing AI hallucinations", "Bing AI responses", "Bing AI experience",
    "Bing AI sucks", "Bing AI broken", "Bing AI is bad", "Bing AI issues", "Bing AI complaints",
    "Bing AI is good", "Bing AI best features", "Bing AI better than Google", "Bing AI useful", "Bing AI innovation",
    "Bing AI is biased", "Bing AI censorship", "Bing AI political bias", "Bing AI filtering content",
    "Bing API", "Bing search API", "Bing AI API", "Microsoft Search API", "Bing API pricing", "Bing API vs Google API",
    "Bing AI speed", "Bing AI slow", "Bing AI fast", "Bing AI lag", "Bing AI updates",
    "Bing search ranking", "Bing AI SEO", "Bing AI content generation", "Bing AI for SEO", "Bing AI results",
    "Microsoft Edge AI vs Chrome AI", "Edge AI vs Google AI", "Bing AI vs Google AI", "Edge AI vs Bard",
    "Bing AI for research", "Bing AI for students", "Bing AI for work", "Bing AI for learning", "Bing AI in business",
    "Bing AI adoption", "Bing AI market share", "Bing AI usage", "Bing AI user growth", "Bing AI competitors",
    "Bing AI image search", "Bing AI video search", "Bing AI visual search", "Bing AI media", "Bing AI DALL-E",
    "Future of Bing AI", "Bing AI roadmap", "Bing AI 2025", "Bing AI next update", "Bing AI in 10 years",
    "Bing AI and Azure", "Bing AI cloud", "Microsoft AI tools", "Microsoft AI vision"
]


# List to store extracted data
all_data = []

# Function to fetch posts and comments
def fetch_reddit_data():
    for index, query in enumerate(queries):
        try:
            print(f"Searching for: {query}")

            # Set post limits based on priority of the query
            if index == 0:
                post_limit = 100
            elif index < 10:
                post_limit = 50
            else:
                post_limit = 20

            # Search for posts matching the query
            for submission in reddit.subreddit("all").search(query, limit=post_limit):
                post_data = {
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "subreddit": submission.subreddit.display_name,
                    "url": submission.url,
                    "created_utc": submission.created_utc,
                    "type": "post",
                }
                all_data.append(post_data)

                # Fetch comments from the post
                submission.comments.replace_more(limit=3)  # Avoid too many deep levels
                for comment in submission.comments.list():
                    comment_data = {
                        "title": submission.title,  # Reference post title
                        "selftext": comment.body,
                        "subreddit": submission.subreddit.display_name,
                        "url": submission.url,
                        "created_utc": comment.created_utc,
                        "type": "comment",
                    }
                    all_data.append(comment_data)

            time.sleep(2)  # Avoid rate limits

        except Exception as e:
            print(f"Error while searching for {query}: {e}")
            continue

# Run the scraping function
fetch_reddit_data()

# Convert the data to a DataFrame and save it to CSV
df = pd.DataFrame(all_data)
df.to_csv("bing_reddit_data.csv", index=False)

print("Scraping complete! Data saved to bing_reddit_data.csv")
