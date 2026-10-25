import random
import re

FAQS = {
    "greeting": {
        "patterns": ["hello", "hi", "hey", "good morning"],
        "responses": [
            "Hello! Welcome to SmartAssist. How can I help you?",
            "Hi there! What can I help you with today?"
        ]
    },
    "services": {
        "patterns": ["services", "what do you offer", "what do you do"],
        "responses": [
            "We provide customer support and general assistance."
        ]
    },
    "hours": {
        "patterns": ["working hours", "opening hours", "business hours"],
        "responses": [
            "Our configured support hours are 9 AM to 6 PM, Monday to Friday."
        ]
    },
    "thanks": {
        "patterns": ["thank you", "thanks"],
        "responses": [
            "You're welcome!",
            "Happy to help!"
        ]
    }
}

def get_response(message):
    message = message.lower().strip()
    message = re.sub(r"[^\w\s]", "", message)

    if not message:
        return "Please enter a message."

    for category, data in FAQS.items():
        for pattern in data["patterns"]:
            if pattern in message:
                return random.choice(data["responses"])

    return (
        "Sorry, I couldn't understand your question. "
        "Please ask about our services or working hours."
    )
