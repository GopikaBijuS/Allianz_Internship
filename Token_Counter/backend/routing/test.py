from router import route_model

prompt = input("Prompt: ")

model, prompt_type = route_model(prompt)

print(f"Type : {prompt_type}")
print(f"Model: {model}")