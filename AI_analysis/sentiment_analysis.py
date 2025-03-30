import torch
import pandas as pd
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from datasets import Dataset
from tqdm import tqdm

# Model Name
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment"

# Load Model & Tokenizer
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)

# Load Dataset (Assuming a CSV file with a 'text' column)
df = pd.read_csv("reddit_comments.csv")  # Change to your dataset file
df = df.dropna(subset=["text"])  # Remove empty comments

# Convert to Hugging Face Dataset for Efficient Processing
dataset = Dataset.from_pandas(df)

# Define Sentiment Labels
LABELS = ["Negative", "Neutral", "Positive"]

# Tokenize Function
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

# Apply Tokenization
dataset = dataset.map(tokenize_function, batched=True)

# Move to PyTorch Tensors for Fast Processing
dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])

# Batch Inference Function
def batch_predict(batch):
    with torch.no_grad():
        inputs = {key: batch[key].to(device) for key in ["input_ids", "attention_mask"]}
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1).cpu().numpy()
        return [LABELS[pred] for pred in predictions]

# Run Inference in Batches
batch_size = 32  # Adjust based on your GPU memory
results = []
for i in tqdm(range(0, len(dataset), batch_size), desc="Processing"):
    batch = dataset[i : i + batch_size]
    results.extend(batch_predict(batch))

# Save Results to CSV
df["sentiment"] = results
df.to_csv("reddit_comments_with_sentiment.csv", index=False)

print("Sentiment Analysis Completed! ✅ Results saved to reddit_comments_with_sentiment.csv")
