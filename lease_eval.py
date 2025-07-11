import os
from openai import OpenAI
from judgeval.tracer import Tracer
from judgeval.data import Example

# Tracing + OpenAI client
tracer = Tracer(project_name="my_project")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("Please set OPENAI_API_KEY in your environment.")
client = OpenAI(api_key=api_key)

# Agent: ask GPT‑4.1 or any other OpenAI model to simplify text
@tracer.observe(span_type="function")
def simplify_lease(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system",
             "content": "You are a legal assistant who rewrites lease clauses into clear, plain English for tenants."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# Keyword‑based scorer
class KeywordScorer:
    name = "lease_keyword_coverage"

    def __init__(self, keywords):
        self.keywords = [kw.lower() for kw in keywords]

    def score(self, prediction: str, _) -> float:
        text = prediction.lower()
        hits = sum(1 for kw in self.keywords if kw in text)
        return hits / len(self.keywords)


# Example lease clause
lease_clause = """
RENT AND PAYMENTS. Tenant shall pay monthly rent of $1,500 due on the 1st day of each month.
If rent is not received by Landlord by 5:00 p.m. on the 5th calendar day, a late fee of $75 shall apply.
SECURITY DEPOSIT. Tenant shall deposit $1,500 as security against damage or default, refundable within 30 days
after the lease ends, less any lawful deductions. TERMINATION. Either party may terminate this agreement with
30 days’ written notice prior to lease end.
"""

example = Example(
    input=f"Summarize the following lease clause in plain English:\n\n{lease_clause}",
    expected_output="Plain‑English summary covering rent due date, late fees, security deposit, and 30‑day notice.",
)

# required concepts to look for in the summary
keywords = ["$1,500", "1st", "late fee", "security deposit", "30 days' notice"]


# Run evaluation
pred = simplify_lease(example.input)

if pred is None:
    print("LLM returned no response.")
    score = 0.0
else:
    score = KeywordScorer(keywords).score(pred, None)

print("Lease clause summary:\n")
print(pred if pred else "[No response from LLM]")

print("\nRequired keywords:", keywords)
print(f"Keyword coverage score: {score:.2f}")
