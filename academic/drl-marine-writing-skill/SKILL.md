---
name: drl-marine-writing-skill
description: "Write and review DRL marine control papers on dynamic positioning, station-keeping, and trajectory tracking. Covers engineering narrative, learning equations, evidence boundaries, results, conclusions and future work, and chapter organization, with an original OE-related evidence base and separately verified JMSE examples; sample observations are not journal requirements."
---

# Writing Skill: DRL-Based Marine Control Papers (OE / JMSE)
*Scope: simulation-based DRL/learning-based marine control papers. The original
six-paper OE-related evidence base is retained; a separate four-paper JMSE sample
supports the structural and writing observations added in September 2026. These
are observed practices and editorial recommendations, not verified journal rules.*

For JMSE structure, conclusion organization, approximate lengths, and exact source
pages, read [JMSE evidence and revision lessons](references/jmse-writing-evidence.md).
Consult it before claiming that a section layout is typical or required by JMSE.

---

## §0 Evidence Base and Confidence Labels

Every observation in this guide is tagged with one of three labels:

- **[Sample]** — observed in the explicitly named source paper(s); may not
  generalise beyond that sample. Unqualified references to the original six
  papers below do not include the later JMSE sample.
- **[Practice]** — consistent with widely observed academic writing norms across
  engineering journals; not specific to JMSE or OE.
- **[Recommend]** — author's recommendation based on the evidence; not a journal
  rule.

**Source papers (read in full):**

| ID | Citation | Journal |
|----|----------|---------|
| Ov21 | Øvereng et al. 2021 | *Ocean Engineering* 235:109433 |
| Ga22 | Gao et al. 2022 | *Ocean Engineering* 266:112885 |
| Yu23 | Yuan & Rui 2023 | *Computers & Electrical Engineering* 110:108858 |
| Le20 | Lee et al. 2020 | *Ocean Engineering* 216:108053 |
| Sa16 | Sarda et al. 2016 | *Ocean Engineering* 127:305–324 |
| Su24 | Sui et al. 2024 | *Remote Sensing* 16:4142 |

**Additional JMSE sample (targeted section and PDF-page inspection, not a claim
of full-paper technical replication):** Shi & Liu 2020, 8:682; Wang et al. 2021,
9:387; Zhu et al. 2021, 9:1267; Gao et al. 2024, 12:2287. Their tasks span collision
avoidance, roll prediction, path planning, and motion prediction; none is a
matched stern-only DP benchmark. See the linked evidence note for titles, DOIs,
section maps, pages, and coverage. A Sensors paper stored alongside them is not
JMSE evidence.

**Authority boundary:** published examples show what those authors did, not what
a journal requires. In the September 2026 review, the JMSE author-guidelines page
could not be retrieved; no official minimum section count, mandatory Discussion,
or prescribed conclusion length was verified. Verify current instructions before
making a compliance claim. Do not substitute another MDPI journal's instructions
or generic template text for confirmed JMSE policy.

---

## §1 Abstract

### Observed structure [Sample: all six papers]

Five moves, not all requiring their own sentence:

1. Engineering context — what DP or station-keeping is and why it matters for this
   specific scenario.
2. Gap or problem — what current methods cannot do well.
3. What this paper does — the method, the vessel, the comparison.
4. Main result — stated qualitatively or with the most transparent physical numbers.
5. Scope or significance (optional).

All six abstracts fall between roughly 100 and 200 words. This is a sample
observation, not a journal rule; check current author instructions for the target
journal.

### What the examined abstracts do with results [Sample]

- Ov21: "good positioning performance while being energy efficient" — no numbers.
- Le20: "better station-keeping performance without deterioration in its control
  efficiency" — no numbers.
- Ga22: "better performance than the existing popular NMPC method" — no numbers.
- Sa16 is the exception: reports wind speed range (4–5 knots) and lists controllers
  tested. The main result is qualitative ("sliding mode controller performed best
  overall"); the wind-speed range is quantitative test-condition information, not
  a quantitative performance result.
- Su24: "all positioning errors … can converge to predefined performance
  constraints within a prescribed time" — system-property claim, no raw numbers.

**Pattern**: most of these abstracts report results qualitatively. Position error in
metres and heading error in degrees are self-explanatory and may appear. Unexplained
abbreviations or bespoke indices (NCI, IAE without expansion, Pfifty) are harder to
interpret without context. [Recommend]

### Guidance for writing the abstract [Recommend unless labelled otherwise]

- State the engineering problem first in physical terms: actuator constraints,
  environmental loads, nonlinear dynamics. Do not open with an RL tutorial.
- Name the method in plain language. "Distributional off-policy deep reinforcement
  learning" is acceptable technical language; it is not plain English for a general
  marine audience, so follow it with a one-clause application-level explanation.
- Describe test coverage explicitly, e.g. "eight wind directions at each of two
  wind speeds, together with a calm-water case" for 17 distinct conditions. Do not
  imply continuous coverage from a discrete angular grid or count calm directions
  as independent physical cases. [Recommend]
- Results in physical language where possible: "lower steady-state position offset",
  "less propulsor activity to achieve the same station-keeping accuracy". If a number
  must appear, use metres for position and degrees for heading — these need no
  explanation.
- Avoid closing sentences whose only content is meta-commentary on the paper's
  value ("this demonstrates the potential of", "this lays the groundwork for").
  A scope statement or a specific result is more useful. Factual significance
  sentences ("These results quantify…") are acceptable if they say something specific.
  [Recommend]
- Active voice reads faster for contribution statements. "We apply X and compare it
  with Y" is clearer than "X is applied and compared with Y". [Practice]

---

## §2 Introduction

### Observed structure [Sample: Ov21, Le20, Ga22, Sa16, Su24]

Consistent across all five papers that have a conventional introduction:

1. **Opening motivation**: why DP or station-keeping matters operationally.
   Cite one or two foundational references (Fossen, Sørensen). Typically one to
   two paragraphs. No algorithm introductions yet.
2. **Traditional methods survey**: PID, LQG, MPC, backstepping, observer-based.
   Note the limitation that motivates the paper. Ov21 spends roughly two pages
   here before introducing DRL.
3. **DRL / learning methods survey**: recent work on similar problems. Characterise
   each citation briefly: method, vessel, result, gap. Note what the existing work
   does not cover.
4. **Gap statement**: what is missing that this paper addresses — stated as a
   factual observation about the literature.
5. **Contributions**: numbered or bulleted list of three to five concrete,
   falsifiable statements. Each should include what was done and what it delivers.
   "We propose X" without a result or scope claim is weak. [Sample + Practice]
6. **Paper organisation**: one paragraph listing what each section covers.
   Present in Ov21, Le20, Ga22, Sa16. [Sample]

### Common problems to avoid [Practice]

- Opening with "In recent years, X has attracted increasing attention" — generic
  filler; revise to a specific engineering observation.
- Contribution stated as "a novel method is proposed" without a result claim.
- Citing a paper and misrepresenting what it did.
- Prefer concise "First … Second … Third" when sequencing is useful, or remove
  ordinal transitions when the logic is already clear. "Firstly" is not incorrect.
- Reviewing DRL or RL theory before establishing the marine engineering context.
  Marine readers are the primary audience; DRL is the method, not the subject.

---

## §3 Notation and Symbol Conventions

### Observed conventions [Sample: Ov21, Le20]

Both papers open their methods section with a **notation table** listing every
symbol, its physical meaning, and its units. This is common in heavy-mathematics
marine control papers.

### Rules [Recommend unless labelled]

- Define every symbol at or immediately after first use, even if a notation table
  exists. [Practice]
- **NED and body-frame axes**: define explicitly once. Standard: x_b forward, y_b
  starboard, z_b down; x_n North, y_n East, z_n down. [Sample: Ov21 §2.1, Le20 §3]
- **Wind direction convention**: state explicitly whether you use TO (nautical/NED)
  or FROM (meteorological). Fossen (2011) uses TO in NED. Meteorological inputs
  need an explicit 180° conversion. [Practice]
- Use consistent notation throughout. If **ν** denotes body velocities in §2,
  do not silently switch to [u, v, r]^T later without re-linking. [Practice]
- State matrix dimensions on first use: **M** ∈ ℝ^{6×6}. [Sample: Ov21 §2.1]

---

## §4 Materials and Methods

### Section and subsection titles [Recommend]

Prefer noun-phrase titles describing the engineering content rather than internal
research workflow. The following are editorial examples, not quotations from the
source papers:

| Avoid | Use instead | Source |
|---|---|---|
| Problem Setup | Vessel Model and Thruster Configuration | — |
| MDP Formulation | Control Formulation and Training Objective | — |
| Learning Protocol | Training Procedure | — |
| Baseline Methods | Comparison Controllers | — |
| Test Grid | Simulation Test Conditions | — |
| Frozen Evaluation | Held-out Evaluation / Deterministic Evaluation | — |

Ov21, Le20, Ga22, and Sa16 all use noun-phrase titles for subsections. [Sample]

### Vessel model subsection [Sample: Ov21 §2.1, Le20 §3.2, Sa16 §4]

Standard structure observed across the papers:

1. **Reference frame definition** — NED and body-fixed, axes labelled. Ov21 does
   this in the first paragraph before any equation.
2. **Equations of motion** — 3-DOF or 6-DOF Fossen form. Every matrix and vector
   defined in the same paragraph or immediately after. Never defer symbol
   definitions to a later subsection.
3. **Hull and thruster parameters** — summarised in a table with SI units. Cite
   the source of each parameter group: towing-tank data, MSS toolbox, manufacturer
   specification, or simulation setting. [Sample: Sa16 Tables 2–3, Le20 Tables 1–2]
4. **Actuator model** — if a lag or slew limit is applied, describe it here with
   its equation. State whether parameters were identified from hardware or chosen
   as simulation settings.

### Citing parameter sources [Practice]

- Cite the physical source of parameters, not a source-code file. Trace back to
  the vessel model documentation, towing-tank report, or reference model paper.
- For MSS toolbox parameters, cite Fossen (2008) MSS documentation, not the `.py`
  or `.m` file. [Recommend]

### Disturbance and environment subsection [Recommend]

- State wind speed and direction ranges for training and evaluation separately.
- Define the current model (speed formula, direction relative to wind, deflection).
- For aerodynamic loads: give the formula, define every coefficient, and cite the
  coefficient source (OCIMF, Isherwood, or measured data).
- State the FROM/TO conversion for any externally sourced wind data explicitly.

### Control / learning method subsection [Recommend]

- Describe the observation vector element by element with physical units and
  normalisation. State what is fed back from the actuator model.
- Describe the action vector and its mapping to physical commands.
- Avoid raw ML jargon in the main description; see §8 for substitution list.
- Training settings go in a **parameter table**, not in prose. Prose describes the
  algorithm structure; the table carries the numbers. [Sample: Ov21 Table 3]
- For multi-method comparisons, one paragraph per method, stating implementation
  differences explicitly.

### Learning mechanisms and comparison controllers [Recommend]

- Give enough mathematics to explain the learning mechanism, not just an algorithm
  name: return/value representation, targets, critic update, actor objective, and
  update order when relevant. Define inputs/outputs and connect the expressions.
  Do not reproduce a general RL tutorial or hide every learning equation in an
  appendix. JMSE examples place core learning mathematics in the main text
  [Sample: Zhu2021 pp.4–8; Shi2020 pp.13–14; Wang2021 pp.5–8].
- Trace implementation-specific equations to the actual implementation and the
  original algorithm paper separately. Identify material differences (e.g. current
  versus target actor, clipped versus unclipped targets, stopped gradients,
  cached versus updated statistics); do not claim exact reproduction by name.
- Introduce comparison controllers by their role: conventional feedback reference,
  alternative learning procedure, or related value-estimation method. Describe
  what each does, rather than opening with a list of absent capabilities.
- For PD/PID, give the feedback law, coordinate/sign conventions, gains and units,
  and actual allocation sequence. A clipped pseudoinverse is not automatically a
  constrained optimum; command-angle limiting after selection can change the
  realized force without recomputing the chosen thrust.
- Prefer "reference controller" or "comparison controller" in engineering prose;
  "baseline" is not forbidden journal terminology. State the allocation scheme,
  since comparisons evaluate controller–allocator combinations.
- Describe common settings once, preferably in a table. State controlled variables
  directly rather than asserting that the comparison is "fair".

### Evaluation metrics subsection [Recommend]

- Define each metric with its formula, steady-state window, units, and how it is
  aggregated (per run, per condition, across seeds).
- IAE (integral of absolute error) is used in Ov21 and Yu23 without heavy
  justification; cite those papers.
- Any custom index (NCI or similar) requires: (a) formula, (b) physical
  interpretation ("NCI counts accumulated normalised propulsor-command magnitude;
  lower values indicate less propulsor activity for the same station-keeping
  duration"), (c) a reference value to calibrate scale.
- Percentile statistics (median, 90th percentile) must state the aggregation
  hierarchy: per run → per condition → across seeds.

---

## §5 Results

### Structure observed [Sample: Ov21 §4, Le20 §4, Ga22 §4, Sa16 §5–6]

1. Opening paragraph: which test conditions, which controllers, pointer to the key
   figure or table.
2. Primary quantitative result: cite numbers from the table, interpret in physical
   language.
3. Secondary and stratified results: directional, initial-condition, or regime
   breakdowns. Each group gets its own paragraph or subsection.
4. Training dynamics (if reported): explicitly separated from physical performance.
   Ov21 §4.1 labels training curves as showing learning behaviour, not physical
   capability.
5. Sensitivity or sweep results: their own subsection with a table. Results
   described in physical metric terms, not reward values.

### From numbers to engineering findings [Recommend]

- Organize results by the question answered, not by the order in which experiments
  were run. A useful sequence is aggregate accuracy/activity → initial-condition
  and seed sensitivity → directional behavior → learning progress → reward
  sensitivity, validation selection, and held-out evaluation.
- Lead a paragraph with the finding, use only the numbers needed to establish it,
  then explain its physical meaning. Do not repeatedly read every table row aloud.
- Qualitative claims still need a named metric and comparator. "Lower cumulative
  command magnitude than PPO" is interpretable; "more efficient" may incorrectly
  imply measured energy or fuel. NCI is not energy, thrust work, or azimuth smoothness.
- An aggregate positioning lead does not imply best performance in every direction
  or every metric. Conversely, a local reversal does not erase the aggregate
  finding. Specify which ordering persists on a separate test set.
- State what the observation identifies: a post-transient evaluation window does
  not establish recovery speed; early attainment of a smoothed return threshold
  measures learning progress in simulation interactions, not formal convergence,
  wall-clock efficiency, or position-error sample efficiency.
- Compare reward settings using physical metrics, not returns on different reward
  scales. Selection on validation data must remain distinct from held-out testing.
- Separate derived physical constraints, observed behavior, and causal hypotheses.
  Geometry can explain coupling without establishing the cause of a particular
  learned-policy peak. Algorithm components need ablations/diagnostics for causal
  attribution. A possible allocation failure mechanism is not proven solely by
  a large aggregate error.

### Figures [Sample]

**Trajectory plots** (Sa16 Figs. 6–8, Ov21 Fig. 8):
- NED axes, North up or clearly labelled.
- Time progression by shading (darker = later) or markers at fixed intervals.
- Heading shown at each marker as a triangle or tick.
- Caption: initial condition, disturbance type and magnitude, seed or trial number.

**Polar / directional plots**:
- Wind or current direction on the angular axis (0° = North, clockwise positive).
- Position or heading error on the radial axis in physical units.
- Dashed reference circles at engineering-tolerance values, labelled.
- Vessel outline at true scale in the centre where space permits.

**Training curves** (Ov21 Fig. 7):
- Caption must state the metric plotted, the reward parameters, and what the bands
  represent.
- Do not call them "convergence curves" unless a formal convergence criterion is
  defined.
- Label them as showing training dynamics, not physical performance.

**Caption guidance** [Recommend]: make each caption interpretable without searching
the main text. Include the metric, test conditions, and meaning of error bars or
shading where applicable; identify initial conditions and the selected seed/trial
for illustrative trajectories. Schematics need their own component/flow description,
not irrelevant statistical fields.

---

## §6 Discussion and Future Directions

### Decide the function before choosing the heading [Recommend]

Discussion asks what the findings mean and which questions they open. It is not
necessarily a second results summary, a compulsory limitations list, or exclusively
a future-work section. Mechanism explanation and literature comparison are useful
when they add knowledge; do not add them merely to fill a template.

The original OE-related sample includes interpretation and scope discussion
[Sample: Ov21 §4, Ga22 §5, Le20 §5]. In the four JMSE examples, interpretation is
sometimes embedded in Results, and two terminal sections called Discussion also
perform the conclusion's job. None of these four has both standalone Discussion
and standalone Conclusions. This does not prove that having both is forbidden.

### A forward-looking discussion [Recommend]

Use **finding → implication → unresolved question → targeted future direction**.
A limitation should explain why the question remains open, rather than merely list
things not done. Examples for simulation-based DP papers:

- Reward sensitivity → relation between the objective and physical accuracy →
  task-specific position/heading tolerances and acceptable actuator usage.
- Direction-dependent performance under steady loads → responses to changing
  loads remain untested → time-varying wind/current and irregular waves, including
  separation of low-frequency positioning deviations from wave-frequency motion.
- Simulation evidence → actual plant/measurement conditions remain untested →
  hardware-in-the-loop and controlled vessel trials assessing model mismatch,
  actuator response, sensor noise, and delay.

These are possible directions, not mandatory experiments for every manuscript.
Do not write deployment plans as commitments unless they actually exist.
Material interpretation boundaries (e.g. command activity is not energy) must remain
accurate even when they do not motivate a future experiment.

### Avoid duplicated endings [Recommend]

- If Results already contains interpretation and the remaining Discussion consists
  mainly of future work, consider **Conclusions and Future Work** rather than
  maintaining two sections just to satisfy a generic outline.
- If substantial mechanism/literature synthesis warrants its own Discussion,
  retain it and use a short Conclusions section to close the contribution.
- A two-sentence lead plus three short thematic paragraphs can suit a standalone
  future-oriented Discussion; it is an editorial option, not a JMSE sample norm.
- Keep caveats close to the affected claim, without "we do not claim" lists.
  Do not append an "although" exception merely to counterbalance every positive
  finding when the metric and comparison scope already make it accurate.
- A concise new statement of an overall limitation may legitimately introduce
  future work in the closing section. Do not introduce new experimental evidence
  or a previously unsupported explanation there.

---

## §7 Conclusions and Combined Endings

### Organize rhetorical functions, not a table recap [Recommend]

A useful engineering sequence is:

1. **Specific motivation/problem:** one sentence on the engineering difficulty,
   not a miniature Introduction.
2. **Method and contribution:** what this study actually did. Applying an existing
   algorithm is not inventing it; do not repeat its component equations to create
   an impression of algorithmic novelty.
3. **Qualitative findings:** what the evidence establishes, with metric and
   comparator explicit. Numbers are optional; select only indispensable anchors.
   Avoid re-awarding every comparator its best metric or restating all tables.
4. **Engineering value:** the capability, design insight, or named application
   scenario this work informs. Potential is legitimate when grounded and scoped;
   simulation evidence is not proof of full-scale safety or deployability.

This sequence is informed by the JMSE closing-section analysis, not a journal
requirement. Wang2021 moves from problem through method capability and validation
to application; Zhu2021 recalls method contributions, staged validation, results,
and a specific limitation-to-future-work transition.

### Length and paragraph organization [Sample / Recommend]

The actual JMSE endings are approximately: Shi2020 Discussion **110 words**;
Gao2024 Discussion **306 words**; Wang2021 Conclusions **190 words**;
Zhu2021 Conclusions and Future Work **290 words**. Each is one natural paragraph
(Gao's crosses a page). The first two are not separately titled Conclusions, so
do not present all four as one uniform conclusion convention. PDF tokenization
makes the counts approximate; these are sample sizes, not prescribed limits.

For a combined ending, **about 280–330 words in two paragraphs** is a useful
project-tested option: first summarize the contribution and value, then give
focused future directions. Do not concatenate an entire Discussion with an entire
Conclusion. A standalone contribution-focused conclusion can be shorter, e.g.
170–220 words, when scope and future directions already appear elsewhere.
Neither range is a general JMSE rule.

### Keep impact concrete [Recommend]

- Prefer a named use case or design decision over generic "high engineering value".
  "A simulation-based basis for evaluating control when bow thrusters are
  unavailable" says more than "a promising approach".
- Words such as "potential", "basis", or "foundation" are not prohibited. Remove
  them when empty or repetitive, not simply because they occur. Do not turn
  defensiveness cleanup into a ban on a legitimate contribution statement.
- Do not repeat the abstract verbatim, introduce new results, rank incompatible
  cross-study metrics, or convert a positioning advantage into universal superiority.
- If future work is already integrated here, do not add another limitations or
  future-work section saying the same thing.

---

## §8 ML / RL Terminology and Engineering Equivalents

None of the five simulation/control papers (Ov21, Ga22, Yu23, Le20, Sa16) use the
left-column terms in their main body text when describing physical control
behaviour. Some appear in algorithm-description sections where they are appropriate.

The key principle: use ML terminology when describing the algorithm internals, and
physical/engineering language when describing the control behaviour and results.

| Avoid for physical descriptions | Engineering replacement |
|---|---|
| agent | controller |
| policy | controller, control law |
| policy network | neural network controller |
| episode | simulation run, trial |
| epoch | training iteration (note: in algorithm-description sections "epoch" is acceptable ML terminology; replace only when describing physical control behaviour or evaluation) |
| frozen evaluation | held-out evaluation (data not used in training or selection) *or* deterministic evaluation (stochastic noise replaced by mean output) — these are distinct concepts; choose the right term and define it on first use |
| learning protocol | training procedure |
| baseline (as method name) | comparison controller, reference controller |
| reward shaping | reward design, reward structure |
| at-target (as test label) | vessel at the target position |
| test grid | test conditions, simulation test set |
| validation grid | validation set |
| held-out grid | withheld test set |
| environment-interaction budget | simulation budget, number of simulation steps |
| hyperparameters | training settings |
| MDP formulation (as a section title or when describing the problem to a non-ML audience) | control problem formulation; in algorithm-description sections "MDP formulation" is precise ML terminology and is acceptable |
| replay buffer | experience buffer |
| seed (standalone) | random initialisation seed |
| epoch-test return | training evaluation return |
| reward shaping parameter | reward tolerance, reward design parameter |

**Note on "frozen evaluation"**: this term is ambiguous. Prefer "held-out
evaluation" (data never used in training or parameter selection) or "deterministic
evaluation" (stochastic actions replaced by the mean output), distinguishing these
two different concepts explicitly where both appear.

**When an ML concept has no marine equivalent**: define it once with a physical
interpretation, then use the descriptive phrase. Example: "The distributional
critic — a value network that estimates the full return distribution rather than
its mean — …"

---

## §9 Equations

- Define every symbol at or immediately after first use, even if a notation table
  exists. [Practice]
- Number equations that are referenced more than once. [Practice]
- State SI units for dimensional quantities when first introduced, inline or in the
  parameter table. [Practice]
- State matrix dimensions on first use. [Sample: Ov21 §2.1]
- Subscript discipline: if subscript *r* denotes "relative" in one equation, do
  not use it for "reference" in another. [Recommend]
- Distinguish physical and normalized quantities, commanded and applied actuator
  states, raw and clipped errors, and radians and degrees. Unit-correct notation
  must preserve the actual implementation, including rate normalization. [Practice]
- Keep an equation on one line at normal size when it fits. Measure/render before
  splitting or shrinking; source line breaks do not determine display width.
  Reflow at mathematical structure when a split is needed. [Recommend]
- Define each acronym at first use in the abstract and independently in the main
  text; a later glossary is not a substitute. Do not expand the same acronym at
  every subsection, and spell out rare abbreviations instead. [Recommend]

---

## §10 Tables

- Make units explicit for dimensional columns, e.g. "Position error (m)";
  dimensionless indices should be identified as such, not assigned invented units.
  Compact parameter tables may place units with values. [Recommend]
- Parameter tables should identify name/symbol, value, and unit, using separate
  columns when helpful rather than imposing four columns on every table. Cite
  parameter sources. [Sample: Sa16 Tables 2–3, Le20 Tables 1–2; Recommend]
- Bold/shaded best entries occur in the original sample [Sample: Ga22 Table 2,
  Ov21 Table 3], but emphasis must match the question and comparison group.
  Do not bold entire preferred-method rows by default. [Recommend]
- Preserve a compact Mean (SD) column when useful. A lowest mean and a lowest SD
  convey different findings: emphasize only the intended number within a cell,
  not both automatically. Do not highlight individual seed minima as though
  training seeds were competing methods. In a parameter sweep, a selected setting
  is not necessarily the winner for every metric. [Recommend]
- Do not invent an obligatory "bold indicates best" note; follow journal rules if
  verified, otherwise explain emphasis only when necessary for interpretation or
  requested. Preserve statistical notes. Formatting changes must not change values
  or aggregation. [Recommend]
- Algorithm settings tables: group parameters by function (architecture, learning
  rates, buffer, training schedule) with ruled separators. Do not mix physical
  vessel parameters with training settings in the same table. [Recommend]

---

## §11 Figures

- Make captions self-contained for the figure type: identify metrics, test
  conditions and uncertainty/colour encodings where relevant; explain components
  and flow for schematics. [Recommend]
- Axis labels with units on every plot. No axis should be unlabelled. [Practice]
- Legend entries match the prose: if you call the method "DSAC-T" in the text, the
  legend says "DSAC-T", not "Proposed" or "Ours". [Recommend]
- Use colourblind-safe palettes and encode state with more than hue alone (pair
  with shape, pattern, or label). Check lettering at final printed size. [Practice]

---

## §12 Citations and References

- Every empirical claim about prior work requires a citation. [Practice]
- Cite the original paper that introduced a method, not a textbook describing it.
  [Practice]
- Fossen (2011) is the standard reference for marine craft hydrodynamics, equations
  of motion, coordinate frames, and hydrodynamic coefficient notation. [Sample: all
  five control papers]
- For MSS toolbox vessel model parameters, cite the MSS documentation (Fossen
  2008), not a source-code file. [Recommend]
- For IAE in the DRL-DP context, cite Ov21 and Yu23 as representative uses.
  [Sample]
- Verify every bibliography entry before submission: author names, year, journal
  name, volume, pages. Fabricated or misattributed citations are a post-publication
  correction and retraction risk. [Practice]

---

## §13 Units and Physical Quantities

- SI throughout the paper. Convert knots to m/s explicitly if the source uses knots.
  [Practice]
- Position error in metres in the Results section. Normalised forms (multiples of L)
  belong in reward descriptions or discussion of geometric scale; do not report
  final results only in normalised units. [Recommend]
- Heading error in degrees in results tables; radians are acceptable in equations.
  [Recommend]
- Force in kN, torque in kN·m for ship-scale thrusters. [Practice]
- IAE units: m·s for position IAE, °·s for heading IAE. State the units. [Recommend]
- Custom activity indices: state the normalisation basis and provide a reference
  value to anchor the scale. [Recommend]

---

## §14 Reproducibility and Statistical Reporting

This section summarises what the source papers do and what current practice in
control and DRL papers requires.

### What the source papers do [Sample]

- Sa16 reports multiple field-trial runs and discusses variability between runs.
- Ov21 reports simulation results for one trained model without multi-seed
  statistics.
- Yu23 and Le20 report simulation results for a single trained model.
- None of the six papers report confidence intervals on their main results.

### Recommended practice for DRL-DP papers [Recommend]

**Seeds and statistics**
- Train and evaluate with multiple random initialisation seeds (at least three;
  five or more preferred). Report mean and standard deviation across seeds, not
  the single best or median result.
- Separate seed variability from condition variability in reported statistics.
  A table that mixes both without labelling which axis is which is uninterpretable.
- State the exact seed values used so results can be reproduced independently.
- Compute SD from unrounded seed-level aggregates, not rounded table cells; state
  the convention and distinguish SD from SE. Extra seeds for one method are a
  sensitivity study, not a newly balanced comparison with all methods.
- Trace time windows and aggregation in the generating evaluator, not just column
  names. A full-episode activity field cannot silently become a steady-window NCI;
  do not rescale it by a duration ratio without the time history.
- Label illustrative single-seed diagnostics with their condition subset, window,
  and statistic so they are not mistaken for main-table aggregates. A mean of
  per-run quantiles is not a quantile of pooled samples.
- Withheld evaluation angles may remain within randomized training support. State
  what was held out from evaluation/selection separately from what lies outside
  the training distribution.

**Checkpoint and model selection**
- State which checkpoint was selected for evaluation and why (best validation
  return, final epoch, early-stopping criterion). Choosing the checkpoint that
  scores best on the test set is a form of evaluation leakage.
- If a hyperparameter or reward-design sweep is reported, use a held-out validation
  set for selection and a separate withheld set for the final evaluation. State
  explicitly which set was used for each decision.

**Simulator and software versions**
- State the simulator name and version (or commit hash), the physics integration
  step size, the control-loop frequency, and the random number generator seeding
  strategy. Two runs with the same nominal seed but different step sizes are not
  the same experiment.
- State the framework and algorithm library versions (e.g. Tianshou 2.0.1,
  PyTorch 2.13.0) used for all reported results. Version differences in numerical
  libraries can change outcomes without a code change.

**Random sources**
- Identify all sources of randomness: initial vessel pose, initial disturbance
  phase, environment action noise, network weight initialisation. State which are
  seeded and how.
- If any randomness is left unseeded (e.g. GPU non-determinism), state that
  explicitly and justify why it does not materially affect the reported results.

**Training curves and convergence**
- Show the spread across seeds (shaded band or individual curves), not just the
  smoothed mean.
- Clearly separate training behaviour (reward curves, learning rate schedules)
  from physical performance (position error, heading error, command activity). A
  controller that accumulates higher training reward may have worse physical
  performance; state which claim is being made and with which metric.
- Do not call a training curve a "convergence curve" unless a formal convergence
  criterion is stated and met.

**Code and configuration availability**
- Where journal policy allows, link to a public repository containing the
  simulation environment, training scripts, and the exact configuration files
  used to produce the reported results. This is increasingly expected in
  control-and-learning papers.

---

## §15 Common Review Comments in This Subfield

Based on the patterns in the source papers and general OE/control review practice.
These are not confirmed editorial policies; they are common points that careful
authors address proactively.

- **Undefined symbols**: a recurring clarity problem in mathematical descriptions.
  Define every symbol; no reviewer-frequency ranking is established here.
- **Single-seed or best-of-N results**: reviewers in control journals increasingly
  expect statistical evidence for DRL claims.
- **Missing comparison**: if a classical controller exists for the same scenario,
  include it. All five control papers include a classical reference.
- **Simulation only**: for papers that cannot do sea trials, be explicit about the
  simulation fidelity and its limitations. Reviewers will ask.
- **Reward function not justified**: state why the chosen reward structure and
  parameters were selected, and what a different choice would do.
- **Missing thruster dynamics**: if actuator lag or slew limits are included,
  state the model and its parameters. If they are not included, state that
  explicitly and note the implication.
- **No discussion of failure cases**: report directions or conditions where a
  method performs poorly. Explain supported mechanisms, but do not invent a cause
  when the available diagnostics do not identify it.

---

## §16 Chapter Architecture and Revision Workflow

### Choose boundaries by reader questions [Recommend]

- Count numbered main sections, not subsections or References. The four inspected
  JMSE papers contain two four-section and two five-section structures. One
  31-page paper keeps methods and the ship model together in a long second section.
  Four main sections are not intrinsically too few. [Sample: see evidence note]
- Audit what each section must accomplish before splitting: physical plant and
  environment; control objective and algorithm; training and comparison procedure;
  evaluation; results; final contribution and future directions.
- A plant/environment → control/training/evaluation boundary can clarify a large
  methods section without implying a new algorithm. A method → experimental-design
  boundary is also possible, but keep common training settings and comparator
  definitions coherent across it. Do not aim for equal page counts at the cost of
  logical dependencies.
- Do not add Related Work, an RL tutorial, or a standalone Discussion solely to
  reach five sections. An algorithm-invention paper's component/prior-work split
  may be inappropriate for an application-and-evaluation contribution.
- Preserve semantic labels and update cross-references, overview sentences, floats,
  and numbering when an approved restructuring is implemented. A proposed split
  is not permission to change the manuscript.

### Review and delivery [Recommend]

1. Read the current manuscript and actual target-journal examples; separate their
   literal headings/paragraphs from your inferred rhetorical functions.
2. Agree on the engineering narrative and draft wording before substantive edits
   when the author requests discussion-first collaboration. Do not silently expand
   a wording approval into a methods or experimental redesign.
3. Audit equations, values, units, statistical hierarchy and scope against retained
   evidence. Keep provenance/audit notes outside the manuscript rather than turning
   them into reviewer-facing prose.
4. Compile after editing; inspect rendered affected pages and neighbors, including
   shifted floats/back matter. Check overflows, references, caption attachment,
   equation fit, table order, and stranded headings. A clean build is not a visual
   review or a scientific validation.
5. Keep output paths and review coverage explicit. Commit only intended changes,
   preserve unrelated work, and synchronize the installed skill and its source
   repository when updating reusable guidance. Verify the actual remote and pushed
   commit rather than assuming a project backup is GitHub.

**Editorial lesson:** be confident about findings with clear metrics/comparators,
concrete about engineering potential, and restrained about causal attribution.
Do not turn a preferred style, a short sample, or one author's approved wording
into a universal journal rule.
