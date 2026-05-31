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
    print("Token Count: ",token_count)

except FileNotFoundError:
    print("File not found")
except IndexError:
    print("Please provide a filename as an argument")