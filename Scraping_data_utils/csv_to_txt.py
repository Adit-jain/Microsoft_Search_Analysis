import pandas as pd
import re

df = pd.read_csv(r'C:\Freelancing\Akhil_Microsoft\Microsoft_Search_Analysis\CSVs\google_play_reviews.com.microsoft.emmx.csv')
def clean_text(text):
    # Remove emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        u"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        u"\U0001F700-\U0001F77F"  # Alchemical Symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed Characters
        "]+", flags=re.UNICODE)

    text = emoji_pattern.sub("", text)  # Remove emojis

    # Remove special characters except common punctuation
    text = re.sub(r"[^a-zA-Z0-9.,!?\'\"()\-:; \n]+", "", text)

    return text.strip()

reviews = df.dropna(inplace=True, axis=0, subset=['Review'])
reviews = df['Review'].tolist()
reviews = '\n'.join(reviews)
reviews = clean_text(reviews)
with open(r'C:\Freelancing\Akhil_Microsoft\Microsoft_Search_Analysis\TXTs\google_play_reviews_edge.txt', 'w', encoding='utf-8') as f:
    f.write(reviews)