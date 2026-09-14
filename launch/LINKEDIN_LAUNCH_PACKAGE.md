# Artificial Stupidity - LinkedIn launch package

Prepared for Raymond Anthony Gomez | September 2026

## Positioning decision

### Rival table

| Voice | Strongest argument | Attacks | Surviving principle |
|---|---|---|---|
| Builder | Lead with the working gate and the six real H100 runs. A public artifact earns more trust than a grand theory alone. | Reject a theory-only launch; reject hiding the post-run failure. | Show the machine, the receipts, and the repair. |
| Strategist | Own a precise category: an independent evidence gate for autonomous AI research. | Reject claiming all AI safety; reject centering only the batch-size result. | Name the decision architecture, not just the benchmark. |
| Skeptic | The sample is small, the holdout was not secret, and no general safety benefit was tested. | Reject “proven safe”; reject “nothing else like it.” | Restraint is part of the product's credibility. |
| Operator | Readers need a fast path: summary, code, tests, logs, reproduction command, and clear next action. | Reject a 16-page-only entry point; reject ambiguous setup. | Make verification easier than belief. |
| Market/Audience | The public core builds credibility; paid pilots can address private workflows, custom rules, reporting, and support. | Reject premature pricing; reject giving enterprise labor away indefinitely. | Open proof, paid implementation. |

**Synthesis:** Launch the bounded result as proof of an evidence-first decision architecture. Tell the human story, disclose the failure, credit Karpathy, and invite reproduction. Offer paid pilots only as a restrained closing line.

## Best project title

1. **Artificial Stupidity: An Evidence Gate for Autonomous AI Research** - winner
2. Artificial Stupidity: The Missing Counterforce to Machine Intelligence
3. Artificial Stupidity: From Metric Improvement to Governed Decision

The winner tells a technical reader what exists without asking them to accept the larger theory first.

## Tagline

**Intelligence proposes. Artificial Stupidity challenges. Evidence adjudicates. A human authorizes.**

## Short product description

Artificial Stupidity is a working KEEP / REJECT / ESCALATE evidence gate around an autonomous AI research loop. It preserves raw evidence, checks a sequestered holdout, and keeps machine judgment separate from human authorization.

## Long product description

Artificial Stupidity is an experimental decision boundary for autonomous AI research, built as an additive derivative of Andrej Karpathy's autoresearch. Instead of allowing a single improved metric to certify a candidate, an external gate checks repeatability, sequestered-holdout performance, resource use, critical failures, and human comprehensibility. The public package includes 27 tests, a preregistered six-run H100 experiment, complete raw logs, source snapshots, hashes, a disclosed and repaired post-run import failure, and separate machine and human decisions. It is a bounded research prototype, not a general AI-safety certification.

## LinkedIn profile project entry

**Project:** Artificial Stupidity: An Evidence Gate for Autonomous AI Research  
**Role:** Founder-builder and research director  
**Brand:** A MONAHINGA™ Evidence Project  

I designed and built an independent KEEP / REJECT / ESCALATE gate around an autonomous AI research loop. The system asks whether a metric improvement is repeatable, survives a sequestered holdout, respects resource limits, passes critical checks, and remains understandable enough for named human authorization. I then ran a preregistered six-run H100 experiment, preserved the raw logs and source snapshot, repaired a disclosed post-run import error without rerunning training, and recorded the machine ESCALATE and human KEEP as separate artifacts. The result is public and reproducible within its stated boundaries; it does not claim general AI safety.

**Repository:** `[insert GitHub URL]`

## Recommended launch post

I started with a joke: if we keep building artificial intelligence, maybe we also need Artificial Stupidity.

Then the joke turned into a serious design question:

**Should the same system that proposes an improvement also be allowed to certify it?**

I built a working answer around Andrej Karpathy's autoresearch project:

> Intelligence proposes. Artificial Stupidity challenges. Evidence adjudicates. A human authorizes.

The result is an external evidence gate that can return **KEEP, REJECT, or ESCALATE**. It checks more than the score: repeatability, a sequestered holdout, resource use, critical failures, and whether a named human can understand what changed.

We tested one deliberately simple candidate on an NVIDIA H100 SXM: reduce total batch size from `2**19` to `2**18`.

Under a preregistered six-run protocol:

- median validation BPB improved **0.928%**;
- median protected-holdout BPB improved **0.924%**;
- every candidate beat every baseline on both metrics - **9/9 pairwise wins** each;
- peak VRAM fell **0.337%**;
- all six training runs completed successfully.

And the machine still did **not** approve its own result.

It returned **ESCALATE** because human comprehensibility was intentionally left unknown. I reviewed the one-line change and the evidence, then separately authorized **KEEP**. Both decisions remain in the record.

We also preserved the messy part: after the paid runs finished, the final runner import failed. The logs and hashes were intact, so we reconstructed the decision from the captured source and inputs without more training, documented the repair, fixed the path, and added a regression test.

That is what this project is really about. Not pretending machines never fail. Building a process in which improvement, doubt, evidence, repair, and human authority stay visible.

The public research edition includes the code, 27 tests, raw logs, source snapshots, hashes, dossier, executive summary, and reproduction protocol.

Repository: `[insert GitHub URL]`

I am also open to a small number of paid organizational pilots involving private deployment, customized evidence rules, audit-ready reporting, integration, and support.

Artificial Stupidity is a working research prototype, not a general AI-safety certification. It is built on and clearly credits Andrej Karpathy's MIT-licensed autoresearch project; no endorsement is implied.

**ARTIFICIAL STUPIDITY - A MONAHINGA™ Evidence Project**

#ArtificialIntelligence #AISafety #AIAgents #MachineLearning #OpenSource #ReproducibleResearch #HumanInTheLoop #ResponsibleAI

## Shorter alternate post

What if an AI could improve a metric - but still could not approve itself?

I built Artificial Stupidity, an independent KEEP / REJECT / ESCALATE evidence gate around Andrej Karpathy's autoresearch loop.

In a preregistered six-run H100 experiment, a one-line batch-size candidate improved median validation BPB by 0.928% and a sequestered holdout by 0.924%. Every candidate beat every baseline on both metrics. Yet the machine returned ESCALATE until a named human reviewed the evidence and authorized KEEP.

The public package includes the code, 27 tests, raw logs, hashes, source snapshots, the disclosed repair of a post-run import failure, and the separate machine/human decision record.

The point is not that criticism makes AI safe. The point is that an optimizer should not hold sole authority to certify its own improvement.

Repository: `[insert GitHub URL]`

**ARTIFICIAL STUPIDITY - A MONAHINGA™ Evidence Project**

#AIAgents #AISafety #OpenSource #ReproducibleResearch #ResponsibleAI

## First comment

The fastest verification path is: executive summary -> verified result -> raw logs and hashes -> test suite. I would especially value attempts to reproduce, break, or improve the gate. If you work on autonomous research, evaluation integrity, model oversight, or auditability, I would be glad to compare notes.

## Respectful outreach to Andrej Karpathy

Hi Andrej - your autoresearch project inspired me to ask a complementary question: what happens if the optimizing loop cannot accept its own improvement without an independent evidence gate? I built a small MIT-licensed derivative that preserves your core loop and adds KEEP / REJECT / ESCALATE, a sequestered holdout, raw evidence packaging, and named human authorization. The first preregistered six-run H100 result passed its bounded criteria; the machine still escalated until a human reviewed the one-line change. I have credited your work clearly and made no claim of endorsement. If you are curious, the repository is here: `[insert GitHub URL]`. Either way, thank you for the inspiration - this was the most fun I have had building in a long time.

## Case study

### The problem

Autonomous research loops are good at proposing and optimizing, but a lower target metric does not automatically prove robustness, reproducibility, or human acceptability. If the proposer also controls acceptance, the process can reward persuasive or brittle improvements.

### What I built

I added an external decision gate around a pinned autoresearch baseline. It receives structured evidence, fails closed on malformed or missing required fields, and returns KEEP, REJECT, or ESCALATE. A runner captures the source, environment, hashes, raw logs, validation results, sequestered-holdout results, and machine decision. Human authorization is stored separately.

### What makes it useful

The prototype turns vague caution into inspectable operations. A reviewer can see what changed, what was tested, what failed, why the machine stopped, and who authorized the final decision. The same pattern could be adapted to private agent workflows where auditability and escalation matter.

### What it does not claim

The six-run result is evidence about one candidate, model, dataset, H100 setup, and five-minute budget. It is not proof of universal model improvement or general AI safety. The holdout was sequestered by the harness but not cryptographically secret. The project is not peer reviewed or production hardened.

### Why it matters

As autonomous systems take more actions, organizations need mechanisms that preserve disagreement, provenance, and human authority without reducing every workflow to a vague “human in the loop” label. Artificial Stupidity is a concrete, falsifiable prototype of that boundary.

### Public release

`[insert GitHub URL]`

## Graphic brief

**Headline:** The machine improved the score. It still could not approve itself.

**Composition:** A clean four-stage horizontal flow - Intelligence -> Artificial Stupidity -> Evidence -> Human - above a compact result card showing 0.928% validation improvement, 0.924% holdout improvement, 9/9 wins, and Machine: ESCALATE / Human: KEEP.

**Screenshot guidance:** Use a cropped terminal result showing the final metrics and the separate decision record. Do not show account balances, email tabs, pod IDs, or personal browser details.

**Color and mood:** Deep navy, warm ivory, evidence green, escalation amber. Serious research notebook rather than science-fiction imagery.

**Boundary line:** Bounded H100 research result - not a general AI-safety certification.

## Image-generation prompt

Create a polished LinkedIn launch graphic in a serious evidence-lab style, 16:9 landscape. Deep navy background with warm ivory panels, evidence green accents, and a restrained amber escalation signal. Show a four-stage flow labeled Intelligence, Artificial Stupidity, Evidence, Human. Beneath it, show a compact verified-result card: Validation +0.928%, Holdout +0.924%, Pairwise wins 9/9, Machine ESCALATE, Human KEEP. Headline: “The machine improved the score. It still could not approve itself.” Footer: “ARTIFICIAL STUPIDITY - A MONAHINGA™ Evidence Project.” Add the boundary text “Bounded H100 research result - not a general AI-safety certification.” No robots, brains, comedy graphics, corporate logos, endorsements, or fake terminal text.
