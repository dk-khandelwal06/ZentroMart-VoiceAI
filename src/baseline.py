import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing from your .env file.")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are ZentroMart's AI customer support assistant.
You help customers with deliveries, returns, refunds, cancellations,
products and warranties.

Rules:
- Introduce yourself as an AI assistant in your first response.
- Be polite, concise and professional.
- Never invent company policies, dates, order statuses or refund amounts.
- You do not have access to company documents or order records yet.
- If you cannot verify an answer, clearly say so.
- Do not claim that you have created a ticket or changed an order.
"""

print("ZentroMart AI Support — Baseline Chatbot")
print("Type 'exit' to quit.\n")

while True:
    question = input("Customer: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"{SYSTEM_PROMPT}\n\nCustomer question: {question}"
    )

    print("\nAssistant:", response.text or "Sorry, I could not generate a reply.")
    print()