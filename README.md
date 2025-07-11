# Judgeval Evaluation Demos

This repo contains **two self‑contained demonstrations** of evaluating LLM agents with the [Judgeval](https://github.com/JudgmentLabs/judgeval) SDK:

| Script            | Purpose | Requires paid LLM? |
|-------------------|---------|--------------------|
| `mock_model.py`   | Fully offline demo – no API calls, useful for local dev / CI. | **No** |
| `lease_eval.py`   | Summarises a lease‑agreement clause with GPT‑4 and scores keyword coverage. | **Yes** (OpenAI key) |

---

## 1️⃣ Why Two Examples? 💡

During development, I encountered the issue below, so I first built `mock_model.py` to test tracing, evaluation loops, and custom scorers without incurring any paid calls.  
<img width="1310" height="54" alt="image" src="https://github.com/user-attachments/assets/ddef3b14-c536-4815-8303-c54bfdedbd8e" />


Once the logic was solid, I added `lease_eval.py`, a production‑style example that is *ready to run* on reviewers’ machines once they drop in their own OpenAI key.

---

## 2️⃣ Quick Start 👩‍💻

### Prerequisites

```bash
python -m pip install --upgrade openai judgeval
```

👀 Note: mock_model.py works even if you never set an API key.
lease_eval.py requires OPENAI_API_KEY.

### A. Running the Offline Mock Demo
```
python mock_model.py
```

### B. Running the Lease‑Agreement Evaluation
```
export OPENAI_API_KEY="sk‑xxxxxxxxxxxxxxxxxxxxxxxx"
python lease_eval.py
```
## What Each File Does
| File            | Highlights                                                                                                              |
| --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `mock_model.py` | *Tracer instrumentation*, simple canned agent, `ExactMatchScorer`, manual evaluation loop.                              |
| `lease_eval.py` | GPT‑4 agent, system prompt for plain‑English legal summaries, `KeywordScorer` that checks five critical lease concepts. |
| `README.md`     | You are here.                                                                                                           |
