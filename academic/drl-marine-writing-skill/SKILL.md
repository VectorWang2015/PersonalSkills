# Writing Skill: DRL-Based Marine Control Papers (Ocean Engineering — OE subfield)
*Scope: simulation-based DRL/learning-based control papers for marine vessels —
dynamic positioning, station-keeping, trajectory tracking — targeting Ocean Engineering
and related marine control journals. No JMSE paper is in the evidence base; do not
apply these observations to JMSE without first checking representative JMSE papers
and the journal's own author guidelines.*

---

## §0 Evidence Base and Confidence Labels

Every observation in this guide is tagged with one of three labels:

- **[Sample]** — observed in one or more of the six source papers; may not
  generalise beyond this subfield.
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

**Limitation**: no JMSE paper is in the sample. Observations labelled [Sample]
apply most reliably to simulation-based DRL/control papers in *Ocean Engineering*.
Before submitting to JMSE or a different OE subfield, consult that journal's
current author guidelines and a few recent representative papers.

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
- For test coverage, give enough information to be accurate. "Evaluated under 17
  wind conditions spanning 0–360° at two wind speeds" is more precise than both
  "a 17-condition grid" (opaque) and "a full range" (implies exhaustive or
  continuous coverage). [Recommend]
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
- "Firstly … secondly … thirdly" is non-standard in English engineering writing;
  use "First … Second … Third" or restructure as prose.
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

Titles are noun phrases describing the engineering content, not the research
workflow. Observed examples from the source papers:

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

### Comparison controllers [Recommend]

- Describe a fixed-gain PD or PID reference in terms of gains, feedback variables,
  and what it lacks (integral term, feedforward, observer). This framing appears in
  Le20 and Ov21.
- In marine engineering papers the conventional PID controller is a **reference**
  or **benchmark** — not a "baseline". Baseline is a ML community term. [Sample]
- State the thrust allocation method used with each controller, since different
  controllers may use different allocation schemes.

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

**Caption convention** [Sample: all six papers]: every caption is self-contained.
Required elements: metric, test conditions, what error bars or shading represent,
and for trajectory plots the initial condition and seed.

---

## §6 Discussion

### Structure observed [Sample: Ov21 §4, Ga22 §5, Le20 §5]

1. Lead with the main engineering finding — why the result has the value it does
   and what physical mechanism explains it.
2. Compare to prior work — where does this agree or differ, and why?
3. Explain outliers or anomalies — directional peaks, seed variation, failure
   cases. State the physical mechanism.
4. Scope and limitations — what was not tested, what the results do and do not
   generalise to. In Ov21, limitations appear in §4.3 (Discussion). [Sample: Ov21 §4.3]
   The key point is that limitations should be discussed where the evidence for them
   lives — either in Discussion or, for overall scope boundaries, at the end of
   Conclusion. What does not belong in Conclusion is a first-time explanation of why
   a result is limited; that explanation needs to follow the result in Discussion.
5. Next steps (optional, one sentence).

### Tone [Recommend]

- State what the data shows. Avoid hedging chains: "it may be possible that, under
  certain conditions, the method could potentially…"
- If a result is inconclusive, say so directly: "the available data do not
  distinguish between X and Y."
- Translate metric comparisons into engineering language in the Discussion: "DSAC-T
  required 49% less propulsor activity than PPO to maintain the same station" is
  more informative than citing raw index values alone.

---

## §7 Conclusion

### Structure observed [Sample: all six papers]

One to two paragraphs, 150–300 words.

1. Restate the main findings as factual sentences, in the same order as the
   contributions listed in the Introduction.
2. Scope boundary (one sentence): what vessel, disturbance type, and simulation
   fidelity the conclusions apply to.
3. Future work (one sentence): a specific, actionable next step. Present in all
   six papers. [Sample]

### What the Conclusion must not do [Practice]

- Introduce information not present in Results.
- Repeat the abstract verbatim.
- Overstate scope: if only one vessel model and one disturbance type were tested,
  do not claim generality.
- Vague significance endings: "demonstrates the potential", "lays the groundwork",
  "confirms X is a promising approach". Replace with a factual finding or a
  specific future-work statement.

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

---

## §10 Tables

- Column headers include units without exception: "Position error (m)", not
  "Position error". [Sample: all six papers]
- Parameter tables: parameter name, symbol, value, units — four columns. Cite
  the source of each parameter group in a footnote or caption. [Sample: Sa16
  Tables 2–3, Le20 Tables 1–2]
- Results tables: align numerical columns to the decimal point. Bold or shade the
  best value in each metric column. [Sample: Ga22 Table 2, Ov21 Table 3]
- Algorithm settings tables: group parameters by function (architecture, learning
  rates, buffer, training schedule) with ruled separators. Do not mix physical
  vessel parameters with training settings in the same table. [Recommend]

---

## §11 Figures

- Every figure caption is self-contained. Required: metric, test conditions, what
  error bars or shading represent. [Sample: all six papers]
- Axis labels with units on every plot. No axis should be unlabelled. [Practice]
- Legend entries match the prose: if you call the method "DSAC-T" in the text, the
  legend says "DSAC-T", not "Proposed" or "Ours". [Recommend]
- Use colourblind-safe palettes and encode state with more than hue alone (pair
  with shape, pattern, or label). Ensure interactive hit targets are at least
  44 px. [Practice]

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

- **Undefined symbols**: the single most common technical complaint in
  mathematics-heavy papers. Define every symbol.
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
- **No discussion of failure cases**: a direction or condition where the method
  performs poorly should be reported and explained, not omitted.
