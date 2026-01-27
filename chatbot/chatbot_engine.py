from chatbot.intents import INTENTS
from chatbot.responses import RESPONSES
from chatbot.llm_hf import ask_free_llm


def chatbot_reply(user_message):
    message = user_message.lower()

    # Rule-based responses first
    for intent, keywords in INTENTS.items():
        if any(word in message for word in keywords):
            return RESPONSES[intent]

    # Fallback to free LLM
    return ask_free_llm(user_message)
