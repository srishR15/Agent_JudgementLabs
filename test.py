from judgeval.tracer import Tracer, wrap
from openai import OpenAI

client = wrap(OpenAI())  # tracks all LLM calls
judgment = Tracer(project_name="my_project")

@judgment.observe(span_type="tool")
def format_question(question: str) -> str:
    # dummy tool
    return f"Question : {question}"

@judgment.observe(span_type="function")
def run_agent(prompt: str) -> str:
    task = format_question(prompt)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": task}]
    )
    return response.choices[0].message.content
    
run_agent("What is the capital of the United States?")