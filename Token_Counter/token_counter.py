import tiktoken

Model_pricing = {
    "gpt-4o": 0.005,
    "gpt-4o-mini": 0.00015,
    "gpt-3.5-turbo": 0.002
}

def token_cost_estimator(text,model):

    if model not in Model_pricing:
        print(f"Model '{model}' not found. Please choose from: {','.join(Model_pricing.keys())}")
        return

    encoding = tiktoken.encoding_for_model(model)

    tokens = encoding.encode(text)
    token_count = len(tokens)

    cost_per_1000_tokens = Model_pricing.get(model)

    estimated_cost = (token_count / 1000) * cost_per_1000_tokens

    return {
        "model": model,
        "token_count": token_count,
        "estimated_cost": round(estimated_cost,6)
    }