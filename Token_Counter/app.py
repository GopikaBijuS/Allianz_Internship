import sys
import tiktoken

try:
    filename=sys.argv[1]
    with open(filename,"r") as file:
        text=file.read()

    encoding=tiktoken.get_encoding("cl100k_base")

    tokens=encoding.encode(text)
    print("Tokens: ",tokens)

    token_count=len(tokens)

    cost_per_1000_tokens=0.002
    estimated_cost=(token_count/1000)*cost_per_1000_tokens

    print("Token Count: ",token_count)
    print(f"Estimated Cost: ${estimated_cost:.6f}")

except FileNotFoundError:
    print("File not found")
except IndexError:
    print("Please provide a filename as an argument")