# Report: Insurance Claim Denial Appeal Letter Generator

**Author:** O.J. Idogun  
**Course:** Generative AI for Business — Spring 2026  
**Date:** April 2026

---

## Business Use Case

Hospitals and medical practices lose billions annually to unworked insurance claim denials. Drafting appeal letters is time-consuming, requiring billing specialists to manually research denial codes, craft clinical justifications, and format professional correspondence — often 20-45 minutes per letter. This prototype automates the first-draft generation of denial appeal letters from structured denial inputs, reducing that time to under 30 seconds and allowing specialists to focus on review rather than drafting.

The workflow takes a denial notice (payer, denial code, denial reason, service, and clinical context) and produces a complete, formatted appeal letter ready for specialist review and submission.

---

## Model Selection

**Model used:** Anthropic Claude (`claude-haiku-4-5-20251001`)

Chosen for three reasons: (1) strong performance on structured business writing tasks, (2) low cost and latency suitable for a high-volume denial management workflow, and (3) access via a clean Python SDK. I briefly tested the same prompts using GPT-4o mini via the OpenAI API and found output quality comparable for simple cases, but Claude Haiku performed better on the legal citation task (Case 4, No Surprises Act) without additional prompting.

---

## Baseline vs. Final Prompt: What Improved

| Dimension | Version 1 (Baseline) | Version 3 (Final) |
|---|---|---|
| Letter structure | Inconsistent, no headers | Consistent Re:/Body/Closing format |
| Specificity | Generic boilerplate | Directly addresses the denial code |
| Hallucination (Case 3) | Invented clinical details | Correctly deferred to documentation |
| Legal citations (Case 4) | No statute cited | No Surprises Act named correctly |
| Length calibration | Same length for all cases | Short for admin cases, longer for clinical |

The most impactful single change was adding the instruction: *"Do not invent clinical details. If context is sparse, note that documentation will follow."* This eliminated hallucination in the edge case where no clinical context was provided, which is the highest-risk failure mode in a real deployment.

---

## Where the Prototype Still Fails or Requires Human Review

**Case 5 (sepsis admission, retroactive denial)** is the clearest failure boundary. The model produced a structurally correct letter that referenced Surviving Sepsis Campaign guidelines, but the specific clinical thresholds it cited (e.g., qSOFA score interpretation) would require validation by a physician advisor or clinical coder before submission. Submitting an appeal with inaccurate clinical data could harm the provider's credibility with the payer.

More broadly, any case involving:
- Retroactive authorization disputes
- Clinical necessity arguments requiring ICD-10/CPT coding expertise
- Cases where the denial involves potential fraud or audit flags

...should require mandatory human review before submission. The system is best positioned as a **drafting assistant**, not an autonomous submission engine.

---

## Deployment Recommendation

**Recommended with conditions.** This prototype demonstrates that LLM-generated denial appeals can be structurally sound and time-saving for the majority of administrative denial types (duplicate claims, modifier issues, straightforward medical necessity). The workflow should be deployed with:

1. A mandatory human review step before any letter is submitted
2. Confidence scoring or flagging for cases with sparse context or complex clinical codes
3. A feedback loop where billing specialists rate letter quality to enable prompt refinement over time

The prototype should not be deployed autonomously. It is a force multiplier for billing specialists, not a replacement for clinical judgment.

---

## Real Output Example (Case 1 — Final Prompt v3)

The following is an excerpt from the actual output generated for case_001 (standard medical necessity denial for an MRI):

> "The patient presented with a six-week history of lower back pain accompanied by radiculopathy. Conservative management, including physical therapy, was initiated and pursued without achieving clinical improvement. Under established clinical guidelines, imaging of the lumbar spine is medically appropriate when conservative treatment fails to resolve radicular symptoms..."

This output met all expected criteria: it cited the clinical history, referenced failed conservative treatment, used the correct denial code (CO-50), and maintained a professional tone. Compared to the baseline prompt (v1), which produced generic boilerplate like "we believe this claim should be reconsidered," the final prompt produced a specific, clinically grounded justification ready for specialist review.
