# ARTIFICIAL STUPIDITY

## An independent evidence gate for autonomous AI research

**A MONAHINGA™ Evidence Project**  
Raymond Anthony Gomez | Second edition | September 2026

Working dossier and research prototype. Not peer reviewed. Not a safety certification.

## Central claim

The smarter an AI system becomes, the more persuasive and consequential its mistakes can become. An optimizing system should not hold sole authority to certify its own improvement. Artificial Stupidity is a proposed independent counterforce whose job is to challenge assumptions, preserve uncertainty, seek disconfirming evidence, and escalate decisions that require human judgment.

> Intelligence proposes. Artificial Stupidity challenges. Evidence adjudicates. A human authorizes.

## Executive finding

The phrase "artificial stupidity" has at least a 75-year lineage across machine imitation, game behavior, institutional satire, philosophy, organizational behavior, and AI safety. The record does not show one suppressed, complete discipline. It shows fragmented meanings that never consolidated into an independent, evidence-seeking decision boundary.

This project turns that synthesis into a working prototype. The gate surrounds Andrej Karpathy's autoresearch loop without giving the optimizer authority to edit the acceptance logic. It returns KEEP, REJECT, or ESCALATE.

The project now includes two empirical stages. A first same-H100 PCIe benchmark found a 2.17% median validation improvement from one batch-size change but lacked a protected holdout, so the gate escalated. A later predeclared H100 SXM experiment evaluated three interleaved baseline/candidate pairs on both ordinary validation and a separately stored holdout. Median validation BPB improved 0.928%, median holdout BPB improved 0.924%, every candidate beat every baseline on both metrics, and peak VRAM fell 0.337%. The machine still escalated because human comprehensibility was intentionally unknown. Raymond Anthony Gomez reviewed the one-line change and bounded evidence and authorized KEEP.

## Evidence labels

- **Documented:** directly supported by a cited source or preserved experiment record.
- **Interpretation:** a synthesis connecting documented facts.
- **Counterfactual:** a plausible path that did not demonstrably occur.
- **Proposal:** a design to be tested, not a proven result.

## Historical reconstruction

Alan Turing observed in 1950 that a machine in an imitation game might deliberately introduce mistakes. Later uses of artificial stupidity described believable conversational limitations, intentional mistakes in game agents, and the institutional absurdity produced when automated literalism meets human systems.[1-5]

A 2018 paper by Michaël Trazzi and Roman V. Yampolskiy explicitly proposed "Building Safer AGI by introducing Artificial Stupidity." Their approach sought to keep an AGI near human capability by limiting computation, memory, speed, or adding selected cognitive biases.[6] That is a genuine safety precursor. It is also different from this proposal: capability restriction changes the intelligent system, while an independent counterforce preserves capability and changes who may accept a decision.

Mikael Falk's distinction between stupidity of understanding and stupidity of judgment supplies a conceptual hinge: greater intelligence does not guarantee better judgment.[7] Recent work on self-correction, sycophancy, abstention, and scalable oversight supplies modern mechanisms for the same concern.[10-14]

The defensible novelty is therefore narrow. This project does not claim to coin the phrase or invent criticism, holdouts, abstention, or human oversight. It proposes and implements their synthesis as an independent, non-degrading, evidence-seeking gate with explicit escalation and separate human authorization.

## Why self-review is not enough

Intrinsic self-correction can fail when a model lacks new evidence or an external correctness signal. Huang and colleagues found that self-correction reduced accuracy across their tested reasoning settings.[10] Sharma and colleagues documented sycophantic behavior in which models changed or abandoned answers under user pressure.[11] OpenAI's SimpleQA discussion showed why accuracy alone can hide materially different error and abstention profiles.[12]

These findings do not prove that every model review is useless. They show why review and independence are different properties. A separate label, separate instructions, protected inputs, external tools, and no silent authority to alter the proposal are design requirements, not decorations.

## Operating doctrine

Artificial Stupidity performs eight jobs:

1. Extract assumptions.
2. Seek disconfirming evidence.
3. Generate rival explanations.
4. Separate fact, inference, speculation, and recommendation.
5. Calibrate uncertainty.
6. Inspect second-order effects.
7. Test reversibility.
8. Abstain or escalate when evidence or authority is insufficient.

It is not random error, intentional incompetence, a comic persona, or a universal veto. The challenger can also be wrong. The architecture must make it possible to reject the critic, measure false vetoes, and inspect the cost of caution.

## Executable architecture

The prototype adds a deterministic gate around a pinned autoresearch baseline. It evaluates:

- whether the primary metric improved;
- whether resource use exceeded a configured boundary;
- whether the result repeated;
- whether the result survived a separately stored holdout;
- whether any critical failure was recorded;
- whether the change remained comprehensible to a named reviewer.

Malformed, impossible, or missing required evidence fails closed. The packaged suite contains 27 GPU-free tests. This demonstrates the decision logic, not a general safety benefit.

## First H100 PCIe benchmark

The original configuration and a one-line candidate each ran three times under the fixed five-minute budget on one RunPod NVIDIA H100 PCIe. The candidate halved total batch size from `2**19` to `2**18`. Median validation BPB improved from 1.052944 to 1.030131, or 2.17%, and peak memory fell 0.34%. Every candidate run beat every baseline run.

The metric-only rule said KEEP. Artificial Stupidity said ESCALATE because the package lacked an independent protected holdout. That was not a denial of the measured gain. It was a refusal to let validation certify robustness.

## Predeclared protected-holdout experiment

The follow-up protocol was fixed before execution:

- one NVIDIA H100 SXM;
- three baseline and three candidate runs, interleaved B1/C1/B2/C2/B3/C3;
- the same five-minute training budget per run;
- upstream training shards 00000 through 00009;
- pinned validation shard 06542;
- separately stored holdout shard 06541 outside the upstream data directory;
- 20,971,520 evaluation tokens for validation and for holdout;
- a pass only if every candidate beat every baseline on both metrics;
- no more than 15% peak VRAM growth;
- machine inability to mark human comprehensibility as passed.

### Final result

| Metric | Baseline runs | Candidate runs | Baseline median | Candidate median | Improvement |
|---|---|---|---:|---:|---:|
| Validation BPB | 0.999791, 1.000213, 1.001808 | 0.990674, 0.990934, 0.991104 | 1.000213 | 0.990934 | 0.928% |
| Holdout BPB | 0.998995, 0.999357, 1.001117 | 0.989901, 0.990126, 0.990284 | 0.999357 | 0.990126 | 0.924% |

Every candidate beat every baseline on each metric: 9/9 pairwise validation wins and 9/9 pairwise holdout wins. Even the worst candidate beat the best baseline by 0.869% on validation and 0.872% on holdout. Peak VRAM fell from 45,060.2 MB to 44,908.2 MB. All six runs exited successfully.

The empirical boundary passed.

## The decision chain

The formal machine action remained ESCALATE because `human_comprehensibility` was intentionally unknown. The gate was designed so the training system could not grant its own final acceptance.

On September 13, 2026, Raymond Anthony Gomez reviewed the one-line change, the bounded result, and the preserved evidence and authorized KEEP. The original machine ESCALATE remains preserved separately from the final governed KEEP.

This is not ceremonial human involvement. The system reached the limit of its authority, made the unresolved condition visible, and stopped.

## The failure that improved the evidence story

After all six paid runs and evaluations completed, the runner failed during the final decision import with `ModuleNotFoundError: No module named 'gate'`. The failure was not hidden. The original archive, SHA-256 manifest, raw logs, environment record, source snapshot, and structured partial results verified.

The decision was reconstructed locally from the captured inputs using the captured gate code and configuration. No additional training was performed. The runner import path was fixed and a regression test was added.

This repair does not make the original runner exit successful; its original exit code remains 1. It does show why raw evidence and partial-state packaging matter. A polished result without receipts would have been weaker.

## What the result establishes

The experiment provides strong bounded evidence that halving total batch size improved both validation and the separately stored holdout for this model, data, H100 SXM, software snapshot, and five-minute budget. The outcome cleared a deliberately strict no-overlap boundary across six runs.

The project also demonstrates a working governance pattern: optimization, challenge, evidence, and authorization can be stored as distinct stages, with machine and human decisions independently inspectable.

## What remains unproven

- That the candidate generalizes across models, datasets, hardware, or longer budgets.
- That three runs per arm estimate the full distribution.
- That the holdout was cryptographically secret or adversary-proof.
- That the gate improves consequential safety in real-world domains.
- That automated evidence fields cannot be gamed.
- That human authorization will resist automation bias at scale.
- That the historical search exhausts every earlier use of the phrase.

The holdout was sequestered from training and ordinary validation paths, but it was visible in project code. Future work should add stronger access controls, tamper-evident provenance, blinded domain tasks, false-veto measurement, and independent replication.

## Falsifiable research program

Compare five conditions on matched tasks: AI alone; the same AI with self-critique; a separate critic; an independent critic with tools and protected evidence; and the full system with structured human authorization. Measure consequential error, unsupported claims, calibration, appropriate abstention, false vetoes, reviewer accuracy, time, and cost.

The doctrine should be rejected or revised if the independent conditions do not outperform self-review at matched compute, if criticism mainly blocks correct high-value action, if the optimizer learns to game the gate, or if reviewers defer more after seeing the gate report.

## Public and commercial path

The public edition should remain free to inspect and reproduce because evidence discipline earns credibility through challenge. Commercial value can sit around the public core: private deployment, workflow integration, customized evidence rules, audit-ready reporting, domain-specific evaluation, training, and support.

No paid pilot should be described as a safety certification. The first commercial objective should be a narrowly scoped organizational decision where the evidence boundary, escalation authority, and acceptance test are known in advance.

## MONAHINGA™ relationship

Artificial Stupidity is presented as **A MONAHINGA™ Evidence Project**. MONAHINGA is the publishing and source identity behind a family of evidence-backed investigations: recover scattered evidence, separate documentation from inference, identify contradictions, test rival explanations, preserve receipts, and make the result reviewable.

USPTO serial 99613654 is live/pending in International Class 041 under Section 1(b). Registration has not issued. MONAHINGA™, not the registration symbol, is the correct current usage. The mark does not authenticate the research and does not create ownership over facts, methods, public records, inherited code, or the phrase Artificial Stupidity.

## Conclusion

The strongest conclusion remains deliberately modest: intelligence and judgment are not the same property, and an optimizing system should not hold sole authority to validate its own improvement.

The project began as a joke about super stupidity. It now has a historical dossier, a falsifiable doctrine, an executable gate, 36 tests, two H100 benchmark stages, a predeclared protected-holdout result, raw evidence, a disclosed repair, and a completed machine-to-human authorization chain.

We built intelligence's brain. This project asks whether it also needs an immune system.

## References

1. A. M. Turing, "Computing Machinery and Intelligence," Mind 59(236), 1950. https://doi.org/10.1093/mind/LIX.236.433
2. H. G. Loebner, "In Response," The Computer Museum, 1991. https://tcm.computerhistory.org/Timeline/LoebnerPrize1991.pdf
3. The Economist, "Artificial Stupidity," September 1992. Historical citation verified through Trazzi and Yampolskiy (2018); original article not relied upon for a scientific claim.
4. L. Lidén, "Artificial Stupidity: The Art of Making Intentional Mistakes," AI Game Programming Wisdom 2, 2003. https://www.liden.cc/lars/WEB/Resume/Papers/2003_AIWisdom.pdf
5. P. J. Denning and D. E. Denning, "Artificial Stupidity," Communications of the ACM 47(3), 2004. https://doi.org/10.1145/986213.986246
6. M. Trazzi and R. V. Yampolskiy, "Building Safer AGI by introducing Artificial Stupidity," 2018. https://arxiv.org/abs/1808.03644
7. M. Falk, "Artificial Stupidity," Interdisciplinary Science Reviews 46(1-2), 2021. https://doi.org/10.1080/03080188.2020.1840219
8. D. Amodei et al., "Concrete Problems in AI Safety," 2016. https://arxiv.org/abs/1606.06565
9. N. Shinn, B. Labash, and A. Gopinath, "Reflexion," 2023. https://arxiv.org/abs/2303.11366
10. J. Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet," ICLR 2024. https://arxiv.org/abs/2310.01798
11. M. Sharma et al., "Towards Understanding Sycophancy in Language Models," ICLR 2024. https://arxiv.org/abs/2310.13548
12. OpenAI, "Why language models hallucinate," 2025. https://openai.com/index/why-language-models-hallucinate/
13. J. Engels et al., "Scaling Laws for Scalable Oversight," NeurIPS 2025. https://arxiv.org/abs/2504.18530
14. K. Yamada, "The structural corruption of human-in-the-loop," AI and Ethics 6, 433 (2026). https://doi.org/10.1007/s43681-026-01295-w
15. U.S. National Park Service, "The Plight of Aspen Emerging as a Beneficiary of Wolf Restoration on Yellowstone's Northern Range." https://home.nps.gov/yell/learn/ys-24-1-the-plight-of-aspen-emerging-as-a-beneficiary-of-wolf-restoration-on-yellowstones-northern-range.htm
16. U.S. National Park Service, "The Big Scientific Debate: Trophic Cascades." https://www.nps.gov/articles/the-big-scientific-debate-trophic-cascades.htm
17. Andrej Karpathy, "autoresearch," GitHub, March 2026, MIT License. https://github.com/karpathy/autoresearch
18. I. Christiano, G. Irving, and D. Amodei, "AI safety via debate," 2018. https://arxiv.org/abs/1805.00899
19. Y. Bai et al., "Constitutional AI," 2022. https://arxiv.org/abs/2212.08073
20. Y. Geifman and R. El-Yaniv, "SelectiveNet," ICML 2019. https://proceedings.mlr.press/v97/geifman19a.html
21. R. Ennals, "Artificial stupidity," AI & Society 31, 431-432 (2016). https://doi.org/10.1007/s00146-016-0655-6
22. H. Ma and M. Su, "Artificial stupidity and coping strategies," Organizational Dynamics, 101059 (2024). https://doi.org/10.1016/j.orgdyn.2024.101059

## Research and authorship note

Concept, framing, project direction, and human authorization: Raymond Anthony Gomez. Research synthesis, source checking, drafting, visualization, and prototype implementation were developed through iterative work with ChatGPT. Historical claims should be checked against the cited sources before formal scholarly publication. Experiment claims are tied to the preserved repository evidence.
