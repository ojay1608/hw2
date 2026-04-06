# HW2: GenAI Denial Appeal Letter Generator

## Workflow: Insurance Claim Denial Appeal Letter Drafting

### Who the user is
A healthcare billing specialist or revenue cycle analyst at a hospital or medical practice who receives insurance claim denials and needs to draft professional appeal letters quickly.

### What input the system receives
A structured denial notice including: the denial reason code, payer name, patient/claim reference, and any additional context about the claim.

### What output the system should produce
A professional, concise appeal letter addressed to the insurance payer that references the denial reason, cites medical necessity or billing justification, and requests reconsideration. Output is saved to a timestamped `.txt` file.

### Why this task is valuable enough to automate
Denial management is one of the highest-cost administrative burdens in U.S. healthcare. Hospitals lose an estimated $5M+ per year to unworked denials. Drafting appeal letters manually takes 20-45 minutes per case. A GenAI prototype that produces a strong first-draft appeal in seconds can dramatically reduce turnaround time and increase appeal success rates — which is the core problem AutoMed AI is building toward.

---

## Model Used
**Anthropic Claude** (`claude-haiku-4-5-20251001`) via the Anthropic Python SDK.

Chosen because: fast, inexpensive, and strong at structured business writing tasks. Haiku is ideal for a prototype where cost and latency matter.

---

## How to Run

### 1. Install dependencies
```bash
pip install anthropic python-dotenv
```

### 2. Set your API key
Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_key_here
```

### 3. Run the app
```bash
python app.py
```

The script will process all 5 eval cases and save outputs to the `outputs/` folder.

---

## Repository Structure
```
hw2-oj/
├── README.md          (this file — includes video link)
├── app.py             (main Python prototype)
├── prompts.md         (prompt versions v1, v2, v3)
├── eval_set.json      (5 representative test cases)
└── report.md          (evaluation report)
```

---

## Walkthrough Video
[Video link to be added after recording]
