import sys
import tiktoken

Model_pricing = {
    "gpt-4o": 0.005,
    "gpt-4o-mini": 0.00015,
    "gpt-3.5-turbo": 0.002
}

try:
    filename = sys.argv[1]
    model = sys.argv[2]

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    encoding = tiktoken.encoding_for_model(model)

    tokens = encoding.encode(text)
    token_count = len(tokens)

    cost_per_1000_tokens = Model_pricing.get(model)

    if cost_per_1000_tokens is None:
        print("Unsupported model")
        sys.exit()

    estimated_cost = (token_count / 1000) * cost_per_1000_tokens

    print(f"Model: {model}")
    print(f"Token Count: {token_count}")
    print(f"Estimated Cost: ${estimated_cost:.6f}")

except FileNotFoundError:
    print("File not found")

except IndexError:
    print("Usage: python app.py <filename> <model>")