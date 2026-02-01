from chatbot.llm_hf import generate_llm_response
from chatbot.responses import MEDICAL_KB

def chatbot_reply(user_message: str) -> str:
    msg = user_message.lower()

    # 1️⃣ Rule-based first (SAFE)
    for key, response in MEDICAL_KB.items():
        if key in msg:
            return response

    # 2️⃣ Block dangerous intents
    danger_words = ["medicine", "treat", "cure", "dose", "diagnose"]
    if any(word in msg for word in danger_words):
        return (
            "I cannot provide medical diagnosis or treatment. "
            "Please consult a qualified healthcare professional."
        )

    # 3️⃣ Controlled LLM fallback
    return generate_llm_response(user_message)
