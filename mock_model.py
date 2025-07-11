from judgeval.tracer import Tracer
from judgeval.data import Example


# SET UP TRACING
judgment = Tracer(project_name="my_project")


# MOCK AGENT as the OpenAI API is paid :(
@judgment.observe(span_type="function")
def run_agent(prompt: str) -> str:
    """Return canned answers to demonstrate evaluation."""
    prompt_lower = prompt.lower()
    if "capital of the united states" in prompt_lower:
        return "Washington, D.C."
    elif "calculate 2 + 2" in prompt_lower:
        return "4"
    else:
        return "I don't know"


# CUSTOM EXACT‑MATCH SCORER  (no base‑class quirks)
class ExactMatchScorer:
    name = "exact_match_binary"

    def score(self, prediction: str, reference: str) -> float:
        """1.0 if exact (case‑insensitive) match, else 0.0."""
        return float(prediction.strip().lower() == reference.strip().lower())

# instantiate scorer once
exact_match_scorer = ExactMatchScorer()


# DEFINE EXAMPLES
examples = [
    Example(input="What is the capital of the United States?",
            expected_output="Washington, D.C."),
    Example(input="Calculate 2 + 2",
            expected_output="4"),
    Example(input="What is the color of the sky?",
            expected_output="Blue"),
]


# RUN EVALUATION LOOP MANUALLY
results = []
for ex in examples:
    prediction = run_agent(ex.input)
    score      = exact_match_scorer.score(prediction, ex.expected_output)
    results.append(score)
    print(f"Q: {ex.input}\n→ Pred: {prediction}\n→ Ideal: {ex.expected_output}\n→ Score: {score}\n")

# overall accuracy
accuracy = sum(results) / len(results)
print("───────────────")
print(f"Overall accuracy ({exact_match_scorer.name}): {accuracy:.2%}")
