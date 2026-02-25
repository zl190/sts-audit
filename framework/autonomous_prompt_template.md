# How to Write Prompts for Autonomous AI Work

A practical guide for delegating complex tasks to AI agents that run while you're away. Derived from running overnight experiments on the STS project.

---

## The Five Components

Every good autonomous prompt has five parts. Miss one and the output degrades.

### 1. Context Files (What to read first)

Tell the agent exactly which files to read, with full paths. Don't describe the files — point to them.

**Bad:**
> "Read the paper and the audit results"

**Good:**
> "Read these files first:
> - /home/user/project/paper/paper_v3.md
> - /home/user/project/framework/audit_method.md
> - /home/user/project/framework/claude_quality_gates.md"

**Why it matters:** The agent has no memory of your prior conversations. Everything it needs must be in the prompt or in files you point to. Assume it knows nothing about your project.

### 2. Clear Deliverable (One output file, specified structure)

Tell the agent exactly where to write output and what sections to include.

**Bad:**
> "Analyze the paper and tell me what you find"

**Good:**
> "Write your complete results to /home/user/project/experiments/exp1_results.md
>
> Structure:
> 1. Method — what you did
> 2. Results — with tables
> 3. Analysis — what it means
> 4. Limitations — be honest
> 5. Conclusion"

**Why it matters:** Without a specified output path, the agent might just return text in the conversation (lost if session ends). Without structure, you get a wall of text. The structure also forces the agent to think systematically.

### 3. Constraints / Quality Gates (Rules to follow)

Give the agent rules that prevent common failure modes. These are your CLAUDE.md-style gates for the specific task.

**Bad:**
> "Do a good job"

**Good:**
> "Apply these rules to your own output:
> - If you write an equation, it must be non-trivial (Gate 5)
> - If you cite a paper, state whether its assumptions hold in our context (Gate 2)
> - Every claim must trace to a specific source or data point (Gate 3)
> - If parameters cannot be estimated, say so explicitly"

**Why it matters:** Without constraints, the AI optimizes for what looks good (fluency, completeness) and neglects what IS good (rigor, honesty). This is the credence good dynamic — the same problem the STS paper is about. Constraints shift the optimization target.

### 4. Explicit Honesty Instructions (What to do when stuck)

Tell the agent what to do when it can't do something, instead of letting it fake it.

**Bad:**
> (nothing — the agent will try to produce output regardless)

**Good:**
> "If you cannot formalize something non-trivially, say so rather than faking it.
> Be intellectually honest. Flag anything that's notation-for-intuition vs genuine model.
> In the Limitations section, state what a proper version of this work would require."

**Why it matters:** AI defaults to producing *something* for every task. Without honesty instructions, it will produce plausible-looking but shallow output when it hits its limits. Telling it "it's OK to say you can't" produces much better calibrated output.

### 5. Anti-Patterns (What NOT to do)

Explicitly state failure modes you've seen before.

**Bad:**
> (nothing — the agent will repeat common failure modes)

**Good:**
> "CRITICAL: You (Claude) are both the generator and the auditor. This is a methodological weakness. State this clearly in the limitations section.
> DO NOT inflate results to make the experiment look better.
> DO NOT read files in /experiments/ — those would bias your review."

**Why it matters:** The agent doesn't know what you've seen go wrong before. Telling it about specific failure modes prevents them. This is accumulated knowledge from prior runs.

---

## Template

Copy and adapt this for any autonomous task:

```
You are [role description]. Your task is to [one-sentence goal].

## Context
Read these files first:
- [path/to/file1] (what it contains)
- [path/to/file2] (what it contains)
- [path/to/file3] (what it contains)

## Your Task

### Step 1: [First phase]
[Specific instructions]

### Step 2: [Second phase]
[Specific instructions]

### Step 3: [Third phase]
[Specific instructions]

## Quality Gates
Apply these rules to your own output:
- [Gate 1: specific rule]
- [Gate 2: specific rule]
- [Gate 3: specific rule]

## Honesty Requirements
- If you cannot [specific thing], say so rather than [specific failure mode]
- [Other honesty requirement]

## Anti-Patterns (DO NOT)
- DO NOT [specific failure mode you've seen before]
- DO NOT [another failure mode]

## Output
Write everything to: [exact file path]

Structure:
1. [Section 1]
2. [Section 2]
3. [Section 3]
4. Limitations — be honest about [specific limitation]
5. [Section 5]
```

---

## Worked Examples

### Example 1: Literature Review + Formalization

```
You are working on a research project about [topic]. The paper has
formal gaps that need filling.

## Context
Read these files first:
- /path/to/paper.md (the paper with gaps)
- /path/to/quality_gates.md (apply Gate 5 to your own output)

## Your Task
Read key SOTA papers in [field]. Then attempt to formalize:
1. [Gap 1] — stated verbally but never formalized
2. [Gap 2] — current version is tautological

## Papers to Find and Read
Use WebSearch and WebFetch to find:
- [Author (Year)] — [what they contribute]
- [Author (Year)] — [what they contribute]
Also search for recent (2023-2025) papers on [specific topics].

## Quality Gates
- If you write an equation, it must say something non-trivial
- If parameters cannot be estimated, say so
- Distinguish: proven theorem vs testable hypothesis vs conceptual framework

## Honesty Requirements
If you can't formalize something, say so rather than faking it.

## Output
Write to: /path/to/formalization_draft.md
Structure: Literature Review, Proposed Model, Self-Audit, Remaining Gaps
```

### Example 2: Blind Review

```
You are an independent academic reviewer. You have NO knowledge of
prior audits or issues found.

## Context
Read ONLY: /path/to/paper.md
DO NOT read: /path/to/experiments/ (would bias your review)

## Phase 1: Calibrate
Search the web for review standards in [field].
Define 6-8 review dimensions with 1-5 scoring criteria.

## Phase 2: Blind Review
Score each dimension. Identify specific issues with quotes.
Classify: Critical / Substantive / Cosmetic.

## Phase 3: Overall Assessment
Accept / Revise & Resubmit / Reject, with rationale.
Top 3 strengths. Top 3 weaknesses. Questions for authors.

## Anti-Patterns
DO NOT read prior audit results.
DO NOT be harsh for its own sake — distinguish genuine weaknesses
from stylistic preferences.

## Output
Write to: /path/to/review.md
```

### Example 3: Controlled Experiment

```
You are running Experiment [N]: testing whether [hypothesis].

## Context
Read: /path/to/method.md (experimental design)
Read: /path/to/quality_gates.md (for generating Condition B)

## Design
- Generate [N] items under Condition A (no treatment)
- Generate [N] items under Condition B (with treatment)
- Audit all items blind (shuffled order)

## Controls
- Same topic/scope for all items
- For Condition A, genuinely try — don't sabotage
- For Condition B, genuinely follow gates — don't over-apply

## Anti-Patterns
CRITICAL: You are both generator and auditor. This is a validity
threat. State this in Limitations. Describe what a proper experiment
would require (independent auditors, separate instances, etc).

## Output
Write to: /path/to/exp_results.md
Structure: Design, Generated Items, Blind Audit, Aggregate Results,
Analysis, Limitations, Conclusion
```

---

## Tips for Running Multiple Agents

1. **Launch independent tasks in parallel** — if they don't depend on each other's output, run them simultaneously
2. **Write results to files, not conversation** — files persist even if the session ends
3. **Use background mode** — `run_in_background: true` lets you continue working while agents run
4. **Check progress without blocking** — read the output file to see partial results
5. **Resume if needed** — agents can be resumed with their ID if interrupted

## When NOT to Use Autonomous Agents

- When the task requires your judgment at multiple decision points
- When the output depends on information only you have (preferences, context, taste)
- When the cost of a wrong result is high and not easily detected
- When you need to iterate quickly (faster to do it in conversation)

The sweet spot: tasks where you can fully specify the inputs, the method, and the output format — and where the agent can self-assess quality using explicit criteria.
