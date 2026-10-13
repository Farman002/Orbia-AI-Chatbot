
import ollama

from database import get_messages, save_message

MODEL = "llama3.2"

SYSTEM_PROMPT = """
You are a helpful AI assistant.
Answer questions clearly and accurately.
Use the conversation history to understand follow-up questions.
If you are unsure about something, say so.
"""


def get_ai_response(conversation_id, user_message):
    """Generate a local AI response and save the conversation."""

    user_message = user_message.strip()

    if not user_message:
        raise ValueError("Message cannot be empty.")

    # Save the user's question in SQLite
    save_message(conversation_id, "user", user_message)

    # Retrieve the conversation history
    history = get_messages(conversation_id)

    # Prepare messages for the local AI model
    api_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    api_messages.extend(
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in history
    )

    # Generate a response locally using Ollama
    response = ollama.chat(
        model=MODEL,
        messages=api_messages
    )

    answer = response["message"]["content"].strip()

    if not answer:
        raise RuntimeError("The AI returned an empty response.")

    # Save the AI response in SQLite
    save_message(conversation_id, "assistant", answer)

    return answer
