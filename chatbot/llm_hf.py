from transformers import pipeline

# Lightweight free model (no API key)
generator = pipeline(
    "text-generation",
    model="distilgpt2"
)

def ask_free_llm(user_message):
    prompt = (
        "You are a medical assistant chatbot. "
        "Give general health information only. "
        "Do not provide prescriptions.\n\n"
        f"User: {user_message}\nAssistant:"
    )

    output = generator(
        prompt,
        max_length=80,
        num_return_sequences=1
    )

    response = output[0]["generated_text"]
    return response.split("Assistant:")[-1].strip()
