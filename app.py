"""
HW2: Insurance Claim Denial Appeal Letter Generator
Author: O.J. Idogun
Course: Generative AI for Business — Spring 2026

This script reads eval cases from eval_set.json, runs each through
the Anthropic Claude API using the final prompt (v3), and saves
the output letters to the outputs/ directory.
"""

import json
import os
from datetime import datetime
from dotenv import load_dotenv
import anthropic

# Load API key from .env file
load_dotenv()

# ─── CONFIGURABLE SYSTEM PROMPT (Version 3 — Final) ───────────────────────────
SYSTEM_PROMPT = """You are an expert medical billing specialist and revenue cycle analyst. You write insurance denial appeal letters that are professional, concise, and persuasive.

Structure every letter as follows:
1. Re: line with claim reference and denial code
2. Opening paragraph: identify the claim, service, and denial reason in 1-2 sentences
3. Justification paragraph(s): directly address why the denial should be overturned, citing the context provided. Be specific. Do not pad with generic language.
4. Closing: one sentence requesting reconsideration and listing any documentation available, followed by a professional sign-off

Calibrate length to complexity. Simple administrative errors (e.g., duplicate claim, modifier issue) should be 1 page or less. Complex clinical necessity cases may be slightly longer.

Important: If the additional context field is empty or sparse, do NOT invent clinical details. Instead, note that supporting clinical documentation will be provided under separate cover and that the appeal is submitted pending that review.

If the case involves federal law (e.g., the No Surprises Act, ERISA), cite the relevant statute by name."""

# ─── USER PROMPT TEMPLATE ─────────────────────────────────────────────────────
def build_user_prompt(case: dict) -> str:
    inp = case["input"]
    return f"""Draft a professional insurance denial appeal letter using the information below.

Payer: {inp['payer']}
Denial Code: {inp['denial_code']}
Denial Reason: {inp['denial_reason']}
Service Denied: {inp['service']}
Claim Reference Number: {inp['patient_ref']}
Billing Provider: {inp['provider']}
Supporting Context: {inp.get('additional_context', 'None provided')}

Produce the complete letter, formatted and ready to submit."""


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    # Load eval set
    with open("eval_set.json", "r") as f:
        eval_cases = json.load(f)

    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Create outputs directory
    os.makedirs("outputs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n{'='*60}")
    print(f"  Denial Appeal Letter Generator — Run: {timestamp}")
    print(f"  Model: claude-haiku-4-5-20251001")
    print(f"  Cases: {len(eval_cases)}")
    print(f"{'='*60}\n")

    results_summary = []

    for case in eval_cases:
        case_id = case["id"]
        case_type = case["type"]
        description = case["description"]

        print(f"Processing {case_id} [{case_type}]: {description}")

        user_prompt = build_user_prompt(case)

        # Make the API call
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )

        output_text = response.content[0].text
        tokens_used = response.usage.input_tokens + response.usage.output_tokens

        # Save output to file
        output_filename = f"outputs/{timestamp}_{case_id}.txt"
        with open(output_filename, "w") as f:
            f.write(f"Case ID: {case_id}\n")
            f.write(f"Type: {case_type}\n")
            f.write(f"Description: {description}\n")
            f.write(f"Expected criteria: {case['expected_output_criteria']}\n")
            f.write(f"Tokens used: {tokens_used}\n")
            f.write(f"\n{'─'*60}\n\n")
            f.write(output_text)

        results_summary.append({
            "case_id": case_id,
            "type": case_type,
            "tokens": tokens_used,
            "output_file": output_filename
        })

        print(f"  Saved to: {output_filename} ({tokens_used} tokens)\n")

    # Print summary
    print(f"\n{'='*60}")
    print("  Run Complete — Summary")
    print(f"{'='*60}")
    for r in results_summary:
        print(f"  {r['case_id']} [{r['type']}] — {r['tokens']} tokens — {r['output_file']}")
    total_tokens = sum(r["tokens"] for r in results_summary)
    print(f"\n  Total tokens used: {total_tokens}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
