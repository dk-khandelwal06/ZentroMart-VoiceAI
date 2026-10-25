
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = Path(r"E:\Capstone_Project_Dataset_FTTT_2026")

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(DATASET_DIR / "tools"))

from rag_pipeline import search_knowledge_base
from tools import lookup_order, create_ticket


class ConversationAgent:
    def __init__(self):
        self.history = []
        self.pending_order_id = None
        self.verification_attempts = 0
        self.verified_order = None

    def reset_verification(self):
        self.pending_order_id = None
        self.verification_attempts = 0
        self.verified_order = None


    def handle(self, message):
        message = message.strip()
        lower = message.lower()

        if not message:
            return "Please enter your question."

        # Handle ticket requests before pending verification.
        # Customers must be able to request human support at any time.
        if any(term in lower for term in [
            "create ticket", "raise a ticket", "human support",
            "human agent", "escalate"
        ]):
            summary = (
                "Customer requested support escalation. "
                f"Customer message: {message}"
            )

            result = create_ticket(
                summary=summary,
                order_id=(
                    self.verified_order.get("order_id")
                    if self.verified_order else None
                ),
                reason="Customer requested escalation",
                intent="support_escalation",
            )

            if result.get("created") is True:
                self.reset_verification()
                return (
                    "Your support ticket has been created. "
                    f"Ticket ID: {result['ticket_id']}"
                )

            return (
                "I couldn't create the ticket: "
                + str(result.get("error", "Unknown error"))
            )

        # Handle pending order verification.
        if self.pending_order_id:
            result = lookup_order(
                self.pending_order_id,
                verification_value=message
            )

            if result.get("verified") and result.get("found"):
                self.verified_order = result
                order_id = self.pending_order_id
                self.pending_order_id = None
                self.verification_attempts = 0

                safe_fields = {
                    "order_id": result.get("order_id"),
                    "order_status": result.get("status"),
                    "order_date": result.get("order_date"),
                    "expected_delivery": result.get("expected_delivery"),
                    "items": result.get("items", []),
                }

                self.history.append({
                    "role": "assistant",
                    "content": f"Verified order {order_id}."
                })

                return (
                    "Verification successful. Available order details:\n"
                    f"{safe_fields}"
                )

            self.verification_attempts += 1

            if self.verification_attempts >= 2:
                self.reset_verification()
                return (
                    "Verification failed. I can't disclose order details. "
                    "You may request a support ticket."
                )

            return (
                "That verification value didn't match. Please try once "
                "more using the registered phone's last 4 digits OR "
                "the delivery PIN code."
            )

        # Start order lookup.
        if "order" in lower and any(ch.isdigit() for ch in message):
            digits = "".join(ch for ch in message if ch.isdigit())

            result = lookup_order(digits)
            self.pending_order_id = result.get("order_id", digits)
            self.verification_attempts = 0

            return (
                "Before I access order details, please verify your identity. "
                "Enter the registered phone's last 4 digits OR the delivery "
                "PIN code. Do not send your full phone number or password."
            )

        # Retrieve relevant knowledge-base passages.
        results = search_knowledge_base(message, top_k=4)

        if not results:
            return (
                "I couldn't find a relevant answer in the knowledge base. "
                "Would you like me to create a support ticket?"
            )

        response_parts = [
            "Relevant ZentroMart knowledge-base information:"
        ]

        for result in results:
            response_parts.append(
                f"\nSource: {result['source']}\n{result['text'][:900]}"
            )

        response_parts.append(
            "\nThese are retrieved policy passages, not a live order check."
        )

        answer = "\n".join(response_parts)
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": answer})

        return answer



def main():
    agent = ConversationAgent()

    print("=" * 55)
    print("ZentroMart Conversation Agent — Local Tool Mode")
    print("Order verification, RAG retrieval and ticket creation")
    print("Type 'exit' to quit.")
    print("=" * 55)

    while True:
        try:
            message = input("\nCustomer: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if message.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        try:
            print("\nAssistant:", agent.handle(message))
        except Exception as error:
            print(f"\nError: {error}")


if __name__ == "__main__":
    main()
