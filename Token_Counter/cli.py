import argparse
from main import token_counter

parser = argparse.ArgumentParser(description="Count tokens and estimate cost for a given text file and model.")
parser.add_argument("filename", type=str, help="Path to the text file to analyze.")
parser.add_argument("model",default="gpt-4o-mini", type=str,help="Model to use for token counting")

if __name__ == "__main__":
    args = parser.parse_args()
    filename = args.filename
    model = args.model

    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found. Please provide a valid file path.")
        exit(1)

    result = token_counter(text, model)
    
    if result:
        print(f"Model: {result['model']}")
        print(f"Token Count: {result['token_count']}")
        print(f"Estimated Cost: ${result['estimated_cost']:.6f}")