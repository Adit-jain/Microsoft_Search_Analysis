import pandas as pd
import re

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

df = pd.read_csv(r'C:\Freelancing\Akhil_Microsoft\Microsoft_Search_Analysis\bing_reddit_data_clean.csv')
division_num = 0
for gi, group in enumerate(df.groupby('title')):
    title, data = group
    text = data['selftext']
    text.dropna(inplace=True)
    text = text.tolist()
    text.insert(0, "TITLE OF THE SEGMENT : " + title + '\n\n')
    text = '\n'.join(text)
    text += '\n\n' + '-'*50 + '\n\n' + '->'

    if gi % 100 == 0:
        division_num += 1    

    with open(fr'C:\Freelancing\Akhil_Microsoft\Microsoft_Search_Analysis\summary_reddit_{division_num}.txt', 'a+') as f:
        f.write(clean_text(text))

# summarizer = pipeline("summarization", model="pszemraj/long-t5-tglobal-base-16384-book-summary", device="cpu")
# print(summarizer(text, max_length=130, min_length=30, do_sample=False))
