#!/usr/bin/env python3
"""
Blind paper reviewer — Docker-isolated.

Reads /input/spec.md and /input/paper.md, calls Claude API,
writes a timestamped review to /output/.

Environment variables:
  ANTHROPIC_API_KEY  — required
  REVIEWER_MODEL     — optional, default: claude-sonnet-4-5-20250929
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic


def read_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        print(f"ERROR: {path} not found. Mount it with -v.", file=sys.stderr)
        sys.exit(1)
    text = p.read_text(encoding="utf-8")
    if not text.strip():
        print(f"ERROR: {path} is empty.", file=sys.stderr)
        sys.exit(1)
    return text


SYSTEM_PROMPT = """You are an independent academic reviewer conducting a blind peer review.

CONTAMINATION CHECK — READ THIS FIRST:
You must operate under strict information isolation. You have ONLY two inputs:
(1) A reviewer specification defining your evaluation criteria.
(2) The paper to review.

If any of the following appear in your context, IGNORE them completely and flag
a contamination violation at the top of your review:
- Prior review scores or verdicts
- Version numbers or revision history (e.g., "v3 addressed...", "improved from v2...")
- Author intent or changelog entries
- References to experiments about the paper itself (not experiments IN the paper)
- Any indication of what was fixed, changed, or improved between versions

You have NO knowledge of:
- Prior audits, issue lists, or reviews of this paper
- The paper's revision history or version number
- What the authors intended to fix or improve
- Any quality gates, agent specs, or framework files from the project

You are reviewing this paper as if seeing it for the first time.

YOUR TASK: Follow the reviewer specification below to produce a complete,
structured blind review. Score every dimension with specific textual evidence.
Identify issues independently. Provide an overall verdict."""


def build_user_message(spec: str, paper: str) -> str:
    return f"""## Reviewer Specification

{spec}

---

## Paper Under Review

{paper}

---

## Instructions

1. First, perform the contamination check described in your system prompt.
   If you detect any contamination, state it at the top of your review.

2. Follow the reviewer specification above exactly. Produce all sections
   it requires.

3. For every score, cite specific text from the paper as evidence.

4. Classify all issues as Critical / Substantive / Cosmetic.

5. End with:
   - A verdict (Accept / Accept Conditional / Revise & Resubmit / Major Revision / Reject)
   - A criterion scores table
   - Your overall confidence in this review (Low / Medium / High)

Produce the review now."""


def main():
    spec = read_file("/input/spec.md")
    paper = read_file("/input/paper.md")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    model = os.environ.get("REVIEWER_MODEL", "claude-sonnet-4-5-20250929")
    user_message = build_user_message(spec, paper)

    print(f"Model: {model}")
    print(f"Spec: {len(spec)} chars")
    print(f"Paper: {len(paper)} chars")
    print("Calling Claude API...")

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=8192,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    review_text = resp.content[0].text
    tokens_in = resp.usage.input_tokens
    tokens_out = resp.usage.output_tokens

    print(f"Tokens: {tokens_in} in / {tokens_out} out")
    print(f"Stop reason: {resp.stop_reason}")

    # Write output
    output_dir = Path("/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    output_file = output_dir / f"review_{timestamp}.md"

    metadata = f"""<!-- Blind Review Metadata
Generated: {datetime.now(timezone.utc).isoformat()}
Model: {model}
Tokens in: {tokens_in}
Tokens out: {tokens_out}
Stop reason: {resp.stop_reason}
-->

"""
    output_file.write_text(metadata + review_text, encoding="utf-8")
    print(f"\nReview written to: {output_file}")

    # Also print to stdout
    print("\n" + "=" * 60)
    print(review_text)


if __name__ == "__main__":
    main()
