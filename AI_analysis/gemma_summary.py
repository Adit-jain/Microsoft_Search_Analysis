import argparse
import textwrap
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

# Set device (CUDA if available, otherwise CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

def load_model_and_tokenizer(model_name):
    """Loads the Gemma model and tokenizer.

    Args:
        model_name (str): The name of the Gemma model to load (e.g., "google/gemma-2b").

    Returns:
        tuple: A tuple containing the model and tokenizer.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to(device)
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model or tokenizer: {e}")
        exit(1)


def split_text(text, max_length=4000):
    """Splits a long text into chunks of a maximum length.

    Args:
        text (str): The input text.
        max_length (int): The maximum length of each chunk.

    Returns:
        list: A list of text chunks.
    """
    sentences = text.split(". ")  # Split into sentences for more meaningful chunks
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 2 <= max_length:  # +2 for ". "
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def generate_summary(model, tokenizer, text, instruction="Summarize the following text:", max_length=512, temperature=0.7, top_p=0.95, num_beams=4, do_sample=True):
    """Generates a summary of the input text using the Gemma model.

    Args:
        model (transformers.PreTrainedModel): The Gemma model.
        tokenizer (transformers.PreTrainedTokenizer): The Gemma tokenizer.
        text (str): The input text to summarize.
        instruction (str): Instruction for the model (e.g., "Summarize the following text:").
        max_length (int): The maximum length of the generated summary.
        temperature (float): The temperature for sampling.  Higher values (e.g., 1.0) make the output more random.
        top_p (float): The top-p value for sampling.
        num_beams (int): The number of beams for beam search.  Higher values improve quality but are slower.
        do_sample (bool): Whether to use sampling (True) or greedy decoding (False).

    Returns:
        str: The generated summary.
    """
    prompt = f"{instruction}\n\n{text}\n\nSummary:"
    input_ids = tokenizer(prompt, return_tensors="pt").to(device)
    try:
        with torch.no_grad():
            output = model.generate(
                input_ids=input_ids["input_ids"],
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_beams=num_beams,
                do_sample=do_sample,
                pad_token_id=tokenizer.eos_token_id
            )
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
        summary = summary.replace(prompt, "").strip() # Remove the prompt from the output
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return ""


def summarize_long_text(model, tokenizer, text, chunk_size=4000, instruction="Summarize the following text:", max_length=512, temperature=0.7, top_p=0.95, num_beams=4, do_sample=True):
    """Summarizes a long text by splitting it into chunks and summarizing each chunk.

    Args:
        model (transformers.PreTrainedModel): The Gemma model.
        tokenizer (transformers.PreTrainedTokenizer): The Gemma tokenizer.
        text (str): The long text to summarize.
        chunk_size (int): The maximum size of each text chunk.
        instruction (str): Instruction for the model for individual chunk (e.g., "Summarize the following text:").
        max_length (int): The maximum length of each chunk summary.
        temperature (float): The temperature for sampling.
        top_p (float): The top-p value for sampling.
        num_beams (int): The number of beams for beam search.
        do_sample (bool): Whether to use sampling (True) or greedy decoding (False).

    Returns:
        str: A summary of the entire text.
    """
    chunks = split_text(text, chunk_size)
    chunk_summaries = []
    for i, chunk in enumerate(tqdm(chunks, desc="Summarizing chunks")):
        chunk_summary = generate_summary(model, tokenizer, chunk, instruction, max_length, temperature, top_p, num_beams, do_sample)
        chunk_summaries.append(chunk_summary)

    # Combine chunk summaries (can be improved with a further summarization step)
    combined_summary = " ".join(chunk_summaries)

    # Optionally, summarize the combined summary for better coherence (recursive summarization)
    combined_summary = generate_summary(model, tokenizer, combined_summary, "Summarize the following summary:", max_length, temperature, top_p, num_beams, do_sample)

    return combined_summary


def main():
    parser = argparse.ArgumentParser(description="Summarize long texts using Gemma.")
    parser.add_argument("text_file", help="Path to the text file to summarize.")
    parser.add_argument("--model_name", default="google/gemma-2b", help="Name of the Gemma model to use.")
    parser.add_argument("--output_file", default="summary.txt", help="Path to the output file for the summary.")
    parser.add_argument("--chunk_size", type=int, default=4000, help="Maximum size of each text chunk.")
    parser.add_argument("--max_length", type=int, default=512, help="Maximum length of the generated summary.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for sampling.")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top-p value for sampling.")
    parser.add_argument("--num_beams", type=int, default=4, help="Number of beams for beam search.")
    parser.add_argument("--instruction", type=str, default="Summarize the following text:", help="Instruction for the model.")
    args = parser.parse_args()

    print("Loading model and tokenizer...")
    model, tokenizer = load_model_and_tokenizer(args.model_name)

    print("Reading text from file...")
    try:
        with open(args.text_file, "r") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.text_file}")
        exit(1)

    print("Summarizing text...")
    summary = summarize_long_text(model, tokenizer, text, args.chunk_size, args.instruction, args.max_length, args.temperature, args.top_p, args.num_beams)

    print("Writing summary to file...")
    try:
        with open(args.output_file, "w") as f:
            f.write(summary)
    except Exception as e:
        print(f"Error writing to file: {e}")

    print(f"Summary saved to {args.output_file}")


if __name__ == "__main__":
    main()