from chatbot.chatbot_engine import chatbot_reply

print("Healthcare AI Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    print("Bot:", chatbot_reply(user_input))
