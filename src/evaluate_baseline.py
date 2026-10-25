import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

DATASET = (
    r"E:\Capstone_Project_Dataset_FTTT_2026"
    r"\practice\questions.csv"
)

df = pd.read_csv(DATASET, dtype=str).fillna("")

results = []

for _, row in df.iterrows():
    question = row["question"]

    prompt = f"""
You are ZentroMart's baseline AI support assistant.
You do NOT have access to company documents or order records.
Never invent policies, order statuses, dates, or amounts.
If you cannot verify an answer, clearly say so.

Customer question: {question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        answer = response.text or ""
        status = "success"
    except Exception as e:
        answer = ""
        status = f"error: {e}"

    results.append({
        "id": row["id"],
        "question": question,
        "expected_decision": row["expected_decision"],
        "reference_answer": row["reference_answer"],
        "baseline_answer": answer,
        "status": status,
    })

    print(f"{len(results)}/{len(df)} completed")

os.makedirs("outputs", exist_ok=True)

output = "outputs/baseline_results.csv"
pd.DataFrame(results).to_csv(output, index=False, encoding="utf-8-sig")

print(f"\nSaved results to {output}")
print("Review the answers before calculating your baseline score.")