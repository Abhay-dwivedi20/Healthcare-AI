from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_API_TOKEN")  # safer than hardcoding

client = InferenceClient(
    model="google/flan-t5-base",
    token=HF_TOKEN
)

SYSTEM_PROMPT = """
You are a healthcare assistant.
Rules:
- Answer in simple English.
- Maximum 3 sentences.
- Educational information only.
- No diagnosis, no treatment, no medicines.
- If question sounds serious, advise seeing a doctor.
"""

def generate_llm_response(user_message: str) -> str:
    prompt = f"""
{SYSTEM_PROMPT}

Question: {user_message}
Answer:
"""
    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=120,
            do_sample=False
        )
        return response.strip()
    except Exception:
        return (
            "I can provide general health information only. "
            "Please consult a qualified doctor for medical advice."
        )
