# Artificial Stupidity — Submission-Readiness Audit

**Audit date:** September 14, 2026  
**Audited release:** `v0.9.0-evidence-prototype`  
**Tagged commit shown by GitHub:** `814e6ff`  
**Audited source archive SHA-256:** `90a319780211343c2736511d9ec4345e29e4a924d389e9f3a93b9e99eadffeb3`  
**Audit posture:** adversarial, evidence-first, no new H100 spending  
**Overall verdict:** **ESCALATE before formal submission; suitable now as a clearly labeled public prototype.**  
**Confidence in verdict:** **0.94**

## Executive verdict

Artificial Stupidity is a real, inspectable research prototype—not merely a slogan or a mockup. Its strongest bounded result is supported: the tagged package contains the six H100 logs, a one-line candidate diff, machine-readable results, working integrity manifests, a machine `ESCALATE`, and a separately recorded author `KEEP`. Independent recalculation from the raw logs reproduces the published medians and percentage changes.

The project is not yet ready to be presented as a hardened independent control system or as a scientifically preregistered study. The gate is separate in the source tree, but its authority boundary is currently enforced mainly by instructions and convention. A generic candidate record can claim that `human_comprehensibility` passed, and anyone able to edit the repository can weaken the gate configuration. The original run also did not capture its Git commit, the exact pre-repair runner is absent from the source snapshot, and the original evidence ZIP whose hash is cited is not itself included. These are repairable engineering and provenance gaps; they do not erase the experiment.

The defensible contribution is therefore narrow and useful: **a concrete, open case study that combines a deterministic KEEP / REJECT / ESCALATE acceptance gate, preserved experiment evidence, explicit uncertainty, and a separately recorded human decision around an autonomous-research loop.** The components have substantial prior art. The particular synthesis and implementation may be useful, but “first,” “unique,” “proven safer,” and “independent” without qualification are not yet supportable.

## What was audited

The audit used the exact GitHub release archive rather than the live `main` branch. It examined 109 files (approximately 3.2 MB), including:

- gate implementation and examples;
- benchmark comparison code and H100 evidence runner;
- all preserved H100 raw logs and structured records;
- repository-wide and nested SHA-256 manifests;
- source snapshots, environment capture, failure and repair records;
- tests, dependency files, Render application, documentation, and launch claims;
- the locally available Git object for the cited upstream Karpathy commit;
- current primary sources describing closely related evaluation, oversight, control, abstention, and venue requirements.

The audit did not repeat the paid H100 experiment and did not treat the live website as proof of the H100 execution.

## System-status matrix

| Component or claim | Classification | Audit finding |
|---|---|---|
| Deterministic KEEP / REJECT / ESCALATE function | **Present and working** | Core gate examples return the expected actions and exit codes. |
| Fail-closed handling of malformed numeric and check-state inputs | **Present and working** | Covered by code and tests; invalid values raise errors rather than becoming approval. |
| Six-run H100 evidence record | **Present and internally consistent** | Six successful logs, metrics, timestamps, hardware record, and hashes are present. |
| Published H100 arithmetic | **Present and verified** | Independent recalculation matches all headline values. |
| Upstream core preserved | **Present and verified** | `prepare.py`, `train.py`, `program.md`, `pyproject.toml`, and `uv.lock` match upstream commit `228791f…` byte-for-byte. |
| Machine and human decisions stored separately | **Present and working as a record** | The machine `ESCALATE` and author `KEEP` are distinct files. |
| Web demonstration | **Present and deployed** | Render deployment is publicly visible; the tagged app has security headers and bounded examples. |
| Gate independence | **Present but procedurally enforced** | Separate code exists, but no OS, signature, permission, or remote-service boundary prevents policy edits. |
| Machine inability to approve human comprehensibility | **Present in the H100 runner, absent in the generic gate contract** | The runner forces `unknown`; generic candidates can supply `pass` and receive `KEEP`. |
| Protected holdout | **Present but weakly protected** | Stored outside training paths and hashed, but public, visible in source, and not access-controlled or blinded. |
| Preregistration | **Partially evidenced** | A predeclared protocol is captured with the run package, but no trusted third-party timestamp or immutable registry proves it preceded observation. |
| Independent human review | **Not present** | The named reviewer is also the project author. This is author authorization, not independent review. |
| Independent reproduction | **Not present** | The evidence is inspectable, but no outside party has repeated the CPU or H100 workflow. |
| Demonstrated safety improvement | **Not tested** | The experiment measures model BPB and evidence-gating behavior, not reduced real-world harm. |
| Cross-domain generality | **Not tested** | One candidate, model, dataset family, metric, and hardware setting were studied. |

## Verification results

### 1. Source and evidence integrity — PASS

- The release archive hash is recorded at the top of this report.
- Every entry in `INTEGRITY_SHA256.txt` verified successfully.
- Every entry in the original H100 evidence `SHA256SUMS.txt` verified successfully.
- The five cited upstream core files exactly match the locally available Git object for Karpathy commit `228791fb499afffb54b46200aca536f79142f117`.
- The baseline and candidate instrumented training files have exactly one functional difference: `TOTAL_BATCH_SIZE = 2**19` versus `2**18`.

**Confidence:** 0.99.

### 2. H100 numerical result — PASS within the stated experiment

Independent parsing of the six raw logs produced:

| Metric, lower is better | Baseline values | Candidate values | Median relative change |
|---|---|---|---:|
| Validation BPB | 0.999791, 1.000213, 1.001808 | 0.990674, 0.990934, 0.991104 | **0.927702% better** |
| Holdout BPB | 0.998995, 0.999357, 1.001117 | 0.989901, 0.990126, 0.990284 | **0.923694% better** |
| Peak VRAM MB | 45,060.2 in all baseline runs | 44,908.2 in all candidate runs | **0.337327% lower** |

Every one of the three candidate scores is below every one of the three baseline scores for validation and holdout. Calling this “9/9 pairwise comparisons” is arithmetically correct. It must not be described as nine independent trials; it consists of nine cross-comparisons formed from three runs per arm. The runs also share a fixed seed and one hardware/software setting, while small variation arises from time-bounded GPU execution.

**Permitted wording:** “Across three runs per arm, every candidate score was lower than every baseline score on both validation and the sequestered holdout.”

**Confidence in arithmetic:** 0.99.  
**Confidence that the effect generalizes:** 0.25.

### 3. Automated tests — PARTIAL PASS

- All Python files compile.
- Eighteen gate and comparison tests passed independently in the audit environment.
- The release contains a preserved successful transcript for all 27 tests.
- A fresh bare Python environment could not collect the remaining nine H100-harness tests because `pyarrow` was not installed. The documented `uv sync` path should install it, but doing so also pulls the full CUDA research environment.
- Flask and Gunicorn are pinned only in `requirements.txt`, not represented in the primary `pyproject.toml` project dependencies or an optional dependency group.
- No GitHub Actions workflow is present to demonstrate clean installation and testing automatically.

This is primarily a packaging and continuous-integration deficiency, not evidence that the nine tests fail. A submission reviewer should not have to infer that distinction.

**Confidence:** 0.91.

### 4. Live application — PASS as demonstration, not as control boundary

The application is read-only with respect to repository state, limits request bodies to 32 KB, catches untrusted evidence errors, and sets sensible content-security, framing, referrer, and MIME headers. It shows the three decision paths clearly.

It accepts user-supplied baseline and candidate JSON and executes the same deterministic gate. It does not authenticate the source of evidence and should therefore be described as an educational evaluator, not a secure authorization service.

**Confidence:** 0.92.

## Claim ledger

| Public claim | Verdict | Confidence | Submission-safe form |
|---|---|---:|---|
| “The package contains a working three-way evidence gate.” | Supported | 0.99 | Use as written. |
| “The H100 medians and percentage improvements are correct.” | Supported for the recorded run | 0.99 | Add “in this six-run experiment.” |
| “9/9 wins” | Supported but easily misunderstood | 0.99 arithmetic / 0.60 interpretation | Say “all nine cross-comparisons from three runs per arm,” or use the clearer permitted wording above. |
| “The upstream core is unchanged.” | Supported for the five declared core files | 0.99 | Name the files and pinned commit. |
| “Complete raw logs and hashes are preserved.” | Mostly supported | 0.94 | Logs and extracted-file hashes are present; do not imply the original ZIP itself is included. |
| “The experiment was preregistered.” | Insufficiently independently timestamped | 0.55 | For v0.9.x say “predeclared protocol captured in the run package.” Use a registry for the next experiment. |
| “The gate is independent/non-editable.” | Overstated | 0.62 | Say “separate from the optimizer in the prototype and governed by instructions.” Reserve “tamper-resistant” for a hardened version. |
| “The machine cannot authorize itself.” | Supported only in the H100 runner path | 0.70 | Say “the H100 runner forces human comprehensibility to unknown.” Harden the generic contract before broader wording. |
| “A human authorized KEEP.” | Supported | 0.99 | Say “the project author reviewed and authorized KEEP.” |
| “An independent human reviewed it.” | Unsupported | 0.99 | Do not say this until an outside reviewer signs. |
| “The result is reproducible.” | Protocol is reproducible in principle; no outside rerun yet | 0.65 | Say “a reproduction package is provided.” |
| “The system improves AI safety.” | Not tested | 0.99 | Say “it operationalizes a testable oversight hypothesis.” |
| “The doctrine or architecture is unique/first.” | Not established | 0.95 | Say “a concrete synthesis and case study,” pending a formal systematic review. |

## Blocking and high-priority findings

### P0 — Enforce the authority boundary in code

The current H100 runner correctly sets `human_comprehensibility` to `unknown`, but `gate.evaluate()` trusts the candidate record's `checks`. The shipped `candidate_keep.json` supplies `human_comprehensibility: pass` and receives `KEEP`. The configuration is also an ordinary editable JSON file. The prose says the optimizer must not edit these items; the operating environment does not enforce that promise.

Required repair:

1. Separate **candidate claims** from **trusted evidence findings**.
2. Make human authorization a distinct signed or hashed artifact that the machine gate cannot populate.
3. Reject or escalate if a candidate supplies reserved fields such as human authorization.
4. Pin and report the policy/configuration digest with every decision.
5. Run the gate in a separate process, account, repository, or service with read-only policy and evidence inputs when making real acceptance decisions.
6. Add adversarial tests for policy edits, evidence substitution, attempted self-authorization, replay, missing digests, and conflicting records.

### P0 — Close the provenance chain

The recorded environment's `git rev-parse HEAD` failed because the H100 directory was not a Git repository. The source snapshot preserves the gate, config, training code, and protocol, but it does not preserve the exact old `h100_evidence_runner.py` that produced the disclosed import failure. The repaired runner now in the repository is not byte-identical to that failed producer. The final decision cites the original evidence ZIP hash `beae2113…`, but that ZIP is not included in the tagged release, so an outside reviewer cannot verify that archive hash directly.

Required repair:

1. Attach the original ZIP to the release if it still exists; otherwise explicitly mark it unavailable.
2. Preserve the exact producer script in every future evidence snapshot.
3. Record a repository commit when available and always record individual source digests.
4. Add a manifest tying raw evidence, derived records, machine decision, human decision, policy digest, and producer version into one chain.
5. Never rewrite v0.9.0; publish repairs as v0.9.1 or later.

### P1 — Tighten scientific language

- Replace “preregistered” with “predeclared in the run package” for the completed experiment unless a trusted pre-run timestamp can be produced.
- Distinguish author authorization from independent human review.
- Describe the public holdout as sequestered from the training and validation paths, not secret or adversary-resistant.
- Treat 9/9 as descriptive cross-comparisons, not independent sample size.
- State that three fixed-seed runs on one system do not estimate broad variability.

### P1 — Repair release metadata and packaging

- `CITATION.cff` says version `1.0.0` while the release is `v0.9.0`.
- `CITATION.cff` still contains `https://github.com/[insert-account]/[insert-repository]`.
- README, executive-summary source, final handoff, and LinkedIn package retain contact or repository placeholders.
- The final handoff still contains pre-publication upload instructions.
- Add a lightweight dependency group for the gate and web demo, separate from the CUDA/H100 research stack.
- Add automated CPU CI for gate tests, H100-harness unit tests, integrity checks, and Flask routes.

### P1 — Measure what the doctrine is supposed to improve

The present experiment demonstrates withholding and evidence capture, but it does not estimate whether the gate catches more consequential mistakes than alternatives or how often it blocks good work. A serious evaluation needs matched conditions:

1. optimizer alone;
2. optimizer plus self-critique;
3. separate critic without protected evidence;
4. external gate with protected evidence;
5. full gate plus structured human authorization.

Measure consequential error, unsupported acceptance, correct rejection, appropriate escalation, false veto, reviewer accuracy, review time, compute cost, and susceptibility to evidence or policy tampering.

## Prior-art position

The central problem is important and active. It is not an empty niche. Several established lines of work overlap materially:

| Prior work | Overlap | Defensible difference in this prototype |
|---|---|---|
| Trazzi & Yampolskiy, *Building Safer AGI by introducing Artificial Stupidity* (2018) | Uses “artificial stupidity” as a safety intervention | Their proposal limits capability; this project attempts to constrain acceptance authority while preserving capability. |
| Selective prediction / abstention | Systems defer when evidence or confidence is insufficient | This gate applies deferral to research-candidate acceptance and records an explicit governance chain. |
| AI safety via debate and Constitutional AI | Structured critique and rule-guided review | This prototype uses a deterministic external rule and protected evidence rather than only model-mediated self-critique. |
| AI Control (Greenblatt et al.) | Separates untrusted capability from monitoring/control protocols and trusted labor | AI Control is substantially deeper on adversarial subversion; this project is a small transparent research-loop case study. |
| Safety and assurance cases | Evidence is organized to justify bounded safety or deployment claims | This project offers executable triage and evidence packaging, but not a complete assurance case. |
| NIST agentic evaluation probes (2026) | Independent evaluators, structured verdicts, trusted corpora, and machine-readable audit trails | NIST is especially close conceptually. Artificial Stupidity adds the branded four-role doctrine and a concrete autoresearch acceptance demonstration. |

**Novelty verdict:** The broad philosophy and individual mechanisms are not novel. The project's possible contribution is the accessible doctrine plus a compact implementation and unusually candid evidence/failure record. A formal novelty claim requires a systematic search and comparison against current agent-evaluation, AI-control, MLOps approval-gate, assurance-case, and human-oversight systems.

**Confidence:** 0.89 that the topic is important; 0.55 that the present synthesis is publishably novel without further study.

Primary sources used for this positioning include [AI Control](https://arxiv.org/abs/2312.06942), [NIST's agentic evaluation probes](https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai), [AI safety via debate](https://arxiv.org/abs/1805.00899), [SelectiveNet](https://proceedings.mlr.press/v97/geifman19a.html), and the references already listed in the dossier.

## Venue readiness

| Venue or audience | Current fit | Readiness decision |
|---|---|---|
| Karpathy `autoresearch` community/discussions | High topical fit, informal | Approach after the P0 boundary and metadata repairs with a concise request for technical criticism, not endorsement. |
| NIST agentic-evaluation-probes initiative | High conceptual fit | Prepare a one-page comparison and a concrete gap/use-case response after hardening. NIST explicitly invites practitioner input. |
| MLCommons AI Risk & Reliability community | Plausible collaboration fit | Seek working-group feedback after publishing reproducible CPU tests and an attack suite. |
| ACM FAccT 2027 | Strong sociotechnical fit | Possible but ambitious. Abstract deadline is October 27, 2026; paper deadline is November 3, 2026. A credible submission needs deeper prior art, adversarial evaluation, human-role analysis, and anonymization. |
| JOSS | Poor immediate timing | Do not submit now. Current criteria emphasize sustained public development, community use, installability, testing, and open-source history; the repository is too new. Reconsider after at least six months of public iteration and outside use. |
| General AI-safety “contest” | No obvious exact-fit priority | Do not reshape the project around a generic contest. Prefer technical communities and review pathways that value evidence and critique. |

Venue facts were checked against the [FAccT 2027 call](https://facctconference.org/2027/cfp.html), [JOSS review criteria](https://joss.readthedocs.io/en/latest/review_criteria.html), [ACM artifact-review guidance](https://www.acm.org/publications/policies/artifact-review-and-badging-current), and [OSF registration guidance](https://help.osf.io/article/330-welcome-to-registrations).

## Ordered roadmap from v0.9.0 to a submission candidate

### Gate 1 — No-cost code and provenance hardening

1. Implement trusted evidence envelopes and reserved-field rejection.
2. Separate machine policy, evidence producer, and human authorization schemas.
3. Pin source, policy, and evidence digests in every decision.
4. Add the missing producer snapshot and explicit original-archive status.
5. Fix placeholders, citation version, URLs, dependency groups, and handoff language.
6. Add CPU continuous integration and web/API tests.

**Spend decision:** Do not buy H100 time yet.

### Gate 2 — No-cost adversarial and ablation suite

1. Attempt self-authorization and policy weakening.
2. Substitute, omit, replay, corrupt, and conflict evidence.
3. Test NaN, infinity, Boolean coercion, duplicate checks, extreme values, and malformed files.
4. Compare optimizer-only, self-critique, separate critic, protected-evidence gate, and human-authorized conditions on synthetic and CPU-real tasks.
5. Report false vetoes as prominently as caught failures.

### Gate 3 — Registered empirical replication

1. Freeze the next protocol in OSF or another immutable, timestamped registry before observing results.
2. Use a clean Git commit and release candidate.
3. Have an outside person execute the instructions without live help.
4. Run a blinded or access-controlled holdout.
5. Only then purchase the minimum H100 time required for the registered rerun.

### Gate 4 — Independent review and second domain

1. Recruit one ML systems reviewer and one governance/human-factors reviewer.
2. Record criticisms, repairs, and unresolved disagreements publicly.
3. Demonstrate the gate on a second low-cost domain where ground truth and error costs are clear.
4. Measure benefit, false veto, time, and cost against simpler alternatives.

### Gate 5 — Submission package

1. Publish v1.0 only after the preceding gates pass.
2. Create an anonymous 12–14-page FAccT-style paper if the evidence supports it.
3. Create shorter technical-review packages for NIST, MLCommons, and the autoresearch community.
4. Keep the LinkedIn post accurate, human-readable, and linked to the frozen release and live demonstration.

## Immediate next micro-step

Build **v0.9.1-hardening** locally from the tagged snapshot. The first change should be a trust-boundary patch that makes candidate-supplied human approval impossible, pins the policy digest, and adds adversarial tests. This is the highest-value task because it converts the project's central doctrine from a promise in prose into an enforceable software property. It is CPU-only and should cost no additional compute money.

## Final assessment

What has been accomplished is meaningful: a striking idea was turned into an executable, falsifiable, publicly inspectable prototype with real experiment receipts and unusually transparent failure documentation in roughly a day. What makes the work potentially valuable is not a claim that it solved AI safety. It is the more disciplined proposition that **a system producing an improvement should not automatically own the evidence rules or the authority to accept that improvement**.

The next version must make that sentence technically true under attack. If v0.9.1 enforces the boundary, v0.9.2 survives adversarial testing, and an outside party reproduces the workflow, the project will have a much stronger basis for serious technical outreach and a credible submission effort.
