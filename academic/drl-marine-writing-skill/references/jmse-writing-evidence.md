# JMSE writing evidence and revision lessons

Updated: 2026-09-22. This note supplements, rather than retrospectively relabels,
the original six-paper OE-related evidence base in `../SKILL.md`.

## 1. Authority and inspection coverage

- **Sample observations:** four locally retained JMSE PDFs, their extracted text,
  main-section/subsection maps, selected learning equations, results analysis, and
  closing sections were examined. Closing pages were directly inspected as images:
  Shi p.18; Wang p.14; Zhu p.14; Gao pp.29–30. Method/learning coverage includes
  Shi pp.13–14, Wang pp.5–8, Zhu pp.4–8, and selected Gao method pages.
- This is **targeted structural and writing evidence**, not a claim that all four
  technical methods, data, citations, and experimental conclusions were validated.
- The PDFs are named below for reproducibility; they are not bundled with the skill.
  DOI links identify the publications, not newly fetched evidence.
- Extracted text for Shi and Gao includes duplicated/overlaid proof text. Count
  actual numbered sections and inspect the rendered page; do not count duplicated
  headings as extra chapters. Page numbers below are PDF page numbers.
- JMSE author instructions at https://www.mdpi.com/journal/jmse/instructions could
  not be retrieved in this review because the fetch rejected the resolved address.
  Search results did not expose enough text to verify the structural provisions.
  **No official minimum chapter count, compulsory separate Discussion/Conclusions,
  or word-limit rule was established.** Verify current guidance independently.
- The neighboring file `sensors-19-04055-v2.pdf` is a Sensors paper and is excluded
  from all JMSE-specific counts and observations here.

## 2. Publications and actual main-section structures

### Shi & Liu (2020), JMSE 8:682

**Deep Learning in Unmanned Surface Vehicles Collision-Avoidance Pattern Based on
AIS Big Data with Double GRU-RNN.**
DOI: https://doi.org/10.3390/jmse8090682
Local source filename: `jmse-08-00682-v2.pdf`; 19 PDF pages.

Four numbered main sections:

1. Introduction, pp.1–3.
2. Materials and Methods, pp.3–15.
3. Results, pp.15–17.
4. Discussion, p.18 (a duplicated extraction layer also places its beginning on p.17).

Methods follows the processing chain: AIS compression → encounter/risk
identification → data normalization → double GRU-RNN. Two-level algorithm detail
sits within the same Methods section. There is no separate Conclusions section.
The terminal Discussion functions predominantly as a contribution summary.

### Wang et al. (2021), JMSE 9:387

**Ship Roll Prediction Algorithm Based on Bi-LSTM-TPA Combined Model.**
DOI: https://doi.org/10.3390/jmse9040387
Local source filename: `jmse-09-00387-v2.pdf`; 16 PDF pages.

Five numbered main sections:

1. Introduction, pp.1–4.
2. Bi-LSTM and TPA Algorithm, pp.4–6.
3. Ship Roll Angle Prediction Algorithm Based on Bi-LSTM-TPA Model, pp.6–8.
4. Simulation Results of Roll Angle Prediction, pp.8–14.
5. Conclusions, p.14.

The method split separates component principles from the combined, application-
specific prediction procedure. Evaluation indicators appear in §4.1, not in a
mandatory standalone experimental-design chapter. Interpretation of difficult
waveform regions and model differences occurs in §4.5, pp.11–14. There is no
standalone Discussion.

### Zhu et al. (2021), JMSE 9:1267

**An Improved Dueling Deep Double-Q Network Based on Prioritized Experience Replay
for Path Planning of Unmanned Surface Vehicles.**
DOI: https://doi.org/10.3390/jmse9111267
Local source filename: `jmse-09-01267-v3.pdf`; 15 PDF pages.

Five numbered main sections:

1. Introduction, pp.1–3.
2. Related Work, pp.3–6.
3. IPD3QN, pp.6–8.
4. Environment Design and Result Analysis, pp.8–14.
5. Conclusions and Future Work, p.14.

The split supports an algorithm-improvement narrative: preceding RL/DQN components
and definitions → IPD3QN refinements and algorithm description. Environment design
and results share one main section. This is not evidence that an application of
an existing algorithm needs a separate RL tutorial or a Proposed Algorithm chapter.

### Gao et al. (2024), JMSE 12:2287

**Online Data-Driven Integrated Prediction Model for Ship Motion Based on Data
Augmentation and Filtering Decomposition and Time-Varying Neural Network.**
DOI: https://doi.org/10.3390/jmse12122287
Local source filename: `jmse-12-02287-v2.pdf`; 31 PDF pages.

Four numbered main sections:

1. Introduction, pp.1–3.
2. Materials and Methods, pp.3–16.
3. Validation Tests of the Integrated Model, pp.16–29.
4. Discussion, pp.29–30.

Methods groups five components: dynamic sliding window, data augmentation,
filtering/decomposition, attention-based prediction, and the ship-motion simulation
model. Validation follows the component organization. A 31-page paper thus retains
four main sections and a long Methods section. Its terminal Discussion summarizes
components and their implications; it has no separately titled Conclusions.

**Structural interpretation:** the explanations above describe the work performed
by the sections. They are not claims about the authors' or editors' private reasons
for choosing that structure.

## 3. Closing-section organization and approximate length

Counts cover prose only, exclude headings/back matter, join PDF line wraps and
hyphenated words where possible, and are approximate rather than journal limits.
All four inspected endings are a single natural paragraph; Gao's spans a page.

| Source / actual heading | Approx. English words | Functional progression |
|---|---:|---|
| Shi, Discussion, p.18 | 110 | research purpose → double-GRU method → trajectory-handling capability → collision-avoidance application |
| Wang, Conclusions, p.14 | 190 | prediction difficulty → combined method → feature-extraction capability → validation and comparative accuracy → operational use |
| Zhu, Conclusions and Future Work, p.14 | 290 | problem/method → functions of refinements → staged tests → overall findings → model/action limitation and next task |
| Gao, Discussion, pp.29–30 | 306 | integrated model → component-specific validation implications → overall prediction capability → application and brief future work |

### What to learn, and what not to copy

- **Wang:** the preceding results paragraph gives percentage error reductions;
  Conclusions compresses them to "better prediction accuracy" rather than reading
  the table again. The closing move connects prediction to a possible operational
  use. Do not copy a leap from prediction accuracy to demonstrated navigation safety.
- **Zhu:** the substantial method recap fits a paper emphasizing algorithmic
  refinements. An application study should recap its actual contribution instead.
  The last part names the mass-point/discrete-action limitation and links it to
  motion modeling/continuous-action research. This is a concrete limitation-to-
  direction link, not an obligation to place all future work in one sentence.
- **Shi:** concise method → capability linkage is useful; broad versatility and
  safety claims are not automatically warranted because they appear in print.
- **Gao:** component-specific implications are stronger than generic praise. Its
  final promise to improve accuracy and robustness is less informative than naming
  what remains untested and how to test it.

None of these four papers has both a separate Discussion and a separate Conclusions.
That observation establishes neither a prohibition nor a requirement. Much of the
substantive interpretation already appears next to the results. Do not insist on
both headings when one combined ending can perform the remaining functions.

## 4. Reusable lessons from the manuscript revisions [Recommend]

These are editorial lessons, not facts discovered in every source paper.

1. **Write toward a reader question.** Motivation → control formulation → testable
   finding is more useful than a chronological account of experiments or an audit
   trail. Paragraphs should add an inference, not merely repeat rankings.
2. **Separate functions before counting sections.** A long Methods section can be
   valid. Split only at a substantive boundary, such as plant/environment versus
   controller/training/evaluation, or method versus comparative study. Keep shared
   settings and notation coherent across the boundary; do not seek equal lengths.
3. **Explain the actual algorithm.** Include core learning equations when necessary
   to understand the mechanism, with implementation-specific targets, gradients,
   state/command meanings and update order. Neither an algorithm name alone nor a
   full textbook tutorial is an adequate methods narrative.
4. **Use exact scientific boundaries rather than defensive rhythm.** Name the
   metric, comparator, and evaluated setting. A local exception belongs where it
   changes interpretation, not after every positive finding. Preserve real limits.
5. **Qualitative does not mean vague.** "Lower aggregate position error and lower
   command magnitude than the named comparator" can be more useful in Conclusions
   than another list of table cells. Activity is not energy; simulation is not sea
   validation; angular holdout is not necessarily out-of-training-support testing.
6. **Keep evidence traceable.** Distinguish raw versus clipped errors, commanded
   versus applied actions, SD versus SE, and per-run versus pooled quantiles.
   Diagnostics on a small condition subset need their own scope/metric definition.
7. **Make the ending purposeful.** Specific motivation → actual method/contribution
   → qualitative findings → concrete engineering value. A combined Conclusions and
   Future Work can use a second short paragraph for unresolved questions. Around
   280–330 words in two paragraphs was useful in this revision, not a universal norm.
8. **Future directions should follow findings.** Reward sensitivity can motivate
   task-defined tolerances; steady-load evidence can motivate changing loads and
   irregular waves; simulation-only evaluation can motivate staged vessel testing.
   This is more informative than listing every omitted experiment.
9. **Allow grounded engineering potential.** Name the intended configuration or
   decision and identify simulation support. Do not ban "potential" or "basis" as
   words, but avoid empty importance claims and unsupported safety/deployment claims.
10. **Typography should preserve meaning.** Bold selected values, not entire favored
    rows; separate a mean winner from an SD winner; preserve Mean (SD) if concise.
    Do not introduce an explanatory boldface note by habit. Fit equations at normal
    size before adding line breaks; use float/space controls for local grouping,
    not to force arbitrary page counts.

## 5. Maintenance boundaries

- Keep the installed skill and its GitHub source synchronized, including this
  reference note; moving only SKILL.md leaves a broken relative link.
- Preserve the original OE-related evidence separately. Do not claim that all
  combined observations came from JMSE or that all source papers were re-audited.
- Publish guidance and source metadata, not unpublished manuscript text, raw
  experimental files, private review conversations, or local credentials.
- When the author requests an assessment, return an assessment. Do not enact a
  chapter split before the author approves the proposed organization.
