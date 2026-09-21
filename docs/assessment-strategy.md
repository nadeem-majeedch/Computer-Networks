# Assessment Strategy

| Field | Value |
|---|---|
| Course | Computer Networks (BS CS / BS DS, Semester 4) |
| Status | Draft v0.1 — awaiting instructor review |
| Companions | [`syllabus.md`](syllabus.md) · [`clo-mapping.md`](clo-mapping.md) · [`lab-strategy.md`](lab-strategy.md) · [`case-study-strategy.md`](case-study-strategy.md) |

## 1. Design principles

1. **Alignment first.** Every instrument maps to CLOs (see [`clo-mapping.md`](clo-mapping.md)
   §2); no instrument exists without a CLO justification, and every CLO except CLO8 is
   measured by at least two instruments.
2. **Assess what the course teaches.** Theory exams test layered-model reasoning and
   analysis, never vendor trivia; labs test the exact packet-analysis and build skills
   rehearsed in class.
3. **Progressive stakes.** Low-stakes frequent signals (exit tickets, quizzes) feed
   forward; high-stakes exams come after students have practiced the same task formats.
4. **Authentic artifacts.** Case studies and the capstone produce work products (traces,
   design documents, dashboards, defense Q&A) rather than only answers.
5. **Workload discipline.** The four heaviest weeks (L13, L19, L20–L23 window, L29) carry
   no additional major deliverables — see the load-balancing notes in
   [`schedule-32-lectures.md`](schedule-32-lectures.md).

## 2. Instruments and weights

| # | Instrument | Type | Timing | Weight | Primary CLOs |
|---|---|---|---|---|---|
| 1 | Quizzes (2 best of 4) | Individual, in-lecture, 15 min | W4, W7, W10, W13 windows | 10% | CLO1–CLO4 |
| 2 | Labs & guided activities (13 deliverables, drop lowest) | Individual/pair | Weekly | 15% | CLO2, CLO4, CLO5 |
| 3 | Subnetting problem set | Individual | Due W8 (L16) | 5% | CLO3 |
| 4 | Midterm examination | Individual, 90 min, in lecture | W8 (L16) | 20% | CLO1–CLO4, CLO6 |
| 5 | Reliable-transport project (LAB-10/11) | Pair | Spec W10, demo W12 | 10% | CLO4, CLO5, CLO6 |
| 6 | Case studies CS-01–CS-03 | Individual | Rolling, W2–W15 | 10% | CLO2–CLO4, CLO6, CLO7 |
| 7 | Capstone (all deliverables) | Team of 3–4 | W13–W16 | 15% | CLO3–CLO8 |
| 8 | Final examination | Individual, cumulative | Finals week | 15% | CLO1–CLO7 |
| | **Total** | | | **100%** | |

## 3. Instrument specifications

### 3.1 Quizzes (10%)
Four 15-minute quizzes in lecture windows (W4, W7, W10, W13); the best two count. Format:
5–8 short items — calculation (subnetting, delay math), dissection (given a packet excerpt,
identify layer/field/anomaly), and one explain-in-two-sentences item. Graded within one
week; answers reviewed in the following lecture. Quiz windows are also the correct trigger
for students to check their own progress against the CLO self-check questions in the CLO
document.

### 3.2 Labs and guided activities (15%)
Thirteen graded lab/GA deliverables across the semester (LAB-01, LAB-02, LAB-03 write-up,
LAB-04 problem set counts separately, LAB-05, LAB-06, LAB-07, LAB-08, LAB-09, LAB-12,
LAB-13, LAB-14, plus GA submissions); the **lowest one is dropped**. Standard rubric
(100 pts): correct results and measurements 40 · analysis/interpretation 30 · evidence
reproducibility (commands, filters, files) 20 · clarity 10. See
[`lab-strategy.md`](lab-strategy.md) §6 for the full rubric and submission format.

### 3.3 Subnetting problem set (5%)
Individual, 8–10 multi-part design questions escalating from mask computation to a
full VLSM plan with aggregation. Released L13, due L16. Rubric: correctness 60 · design
justification 25 · documentation hygiene 15. This is deliberately a *standalone* instrument
because CLO3 is the course's most transferable examinable skill.

### 3.4 Midterm examination (20%)
90 minutes, in lecture (W8, after L16), covering Modules 1–3. Structure:
30% selected-response/short answer (vocabulary, fields, behavior) · 40% problems
(subnetting, delay/throughput calculations, FDB/routing-table reasoning) · 30% trace
analysis (2 packet excerpts: explain what happened and why). A formula sheet is provided;
no devices. Sample paper released one week prior.

### 3.5 Reliable-transport project (10%)
Pairs. Build a reliability layer over UDP (sequencing, ACKs, timeout/retransmit, optional
sliding window for bonus). Deliverables: design spec (graded milestone, W10), working
implementation with protocol-state write-up, and a 10-minute in-lab demo (W12) including a
congestion/loss experiment under `netem`. Rubric: correctness under loss 40 · protocol
design quality 25 · experiment interpretation 20 · code clarity 15.

### 3.6 Case studies CS-01–CS-03 (10%)
Individual write-ups against the scenario packets in
[`case-study-strategy.md`](case-study-strategy.md): CS-01 layered-incident exercise (W2,
graded credit within lab component), CS-02 LAN design with addressing plan (due L16,
4% weight), CS-03 outage diagnosis (evidence log L23, diagnosis L26 3%, RCA report L29
3%). Rubric: evidence quality (real captures cited) 40 · reasoning chain 40 ·
communication 20.

### 3.7 Capstone (15%)
Teams of 3–4, Meridian CS-04 scenario. Stages and weights within the 15%:
design document (W13, 25%) · working build demo (W15 clinic, 20%) · monitoring dashboard +
measurement data (W16, 20%) · final report (W16, 20%) · 15-minute defense presentation with
individual Q&A (W16, 15%). Peer contribution factor ±10% applied per rubric in
[`case-study-strategy.md`](case-study-strategy.md) §5.

### 3.8 Final examination (15%)
Cumulative with emphasis on Modules 4–8. Structure mirrors the midterm plus one synthesis
question (explain an end-to-end flow across all layers, given a scenario). Same formula-sheet
and no-device rules.

## 4. Grading scale and moderation

⚠ VERIFY: adopt the university's official letter-grade boundaries. Recommended internal
bands pending that mapping: A ≥ 85 · A− 80–84 · B+ 75–79 · B 70–74 · C+ 65–69 · C 60–64 ·
D 50–59 · F < 50. Moderation: exam papers sampled by a second instructor; lab rubrics spot-
checked weekly; capstone double-marked (instructor + one external/peer faculty).

## 5. Academic integrity, AI use, and ethics

- **Individual instruments:** quizzes, problem set, exams, and case-study write-ups are
  individual; discussion of concepts is fine, sharing written answers or trace annotations
  is not.
- **Collaborative instruments:** labs (pairs allowed where stated), reliable-transport
  project (pairs), capstone (teams). All listed members must be able to explain any part.
- **Reproducibility rule:** any claimed measurement or capture must be reproducible from
  submitted commands/filters/files; fabricated evidence scores zero on the whole instrument
  and triggers the integrity process.
- **Generative AI:** permitted for code explanation and grammar, not for producing graded
  analysis text or exam answers — ⚠ VERIFY against the program's current AI policy before
  publication.
- **Ethics gate:** the week-1 acknowledgment in [`prerequisites.md`](prerequisites.md)
  governs all capture and attack-emulation work.

## 6. Feedback timeline

| Assessment | Feedback within |
|---|---|
| Exit tickets/GAs | Next lecture (verbal + worked answers) |
| Quizzes | 1 week |
| Labs | 1 week |
| Problem set, midterm | 2 weeks (before course-drop/W-date where applicable) |
| Project milestone & demo | 1 week |
| Case studies | 2 weeks |
| Capstone stages | Stage gates reviewed within 1 week; final within university grade deadline |

## 7. Alignment verification checklist (for the foundation audit)

- [x] Every instrument maps to ≥1 CLO (see [`clo-mapping.md`](clo-mapping.md) §2)
- [x] Every CLO (except CLO8, by design) is measured by ≥2 instruments
- [x] Weights sum to exactly 100%
- [x] Due dates consistent with [`syllabus.md`](syllabus.md) calendar and
      [`schedule-32-lectures.md`](schedule-32-lectures.md) milestone table
- [x] No week carries more than one major deliverable (load-balance rule)
- [x] Exam formats rehearsed beforehand (quiz item styles = midterm item styles)
