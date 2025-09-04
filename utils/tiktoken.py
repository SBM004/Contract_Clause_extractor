import tiktoken

def estimate_token(text):
    encoder=tiktoken.encoding_for_model('gpt-3.5-turbo')

    token=encoder.encode(text)
    return len(token)