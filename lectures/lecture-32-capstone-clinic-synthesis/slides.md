# Lecture 32 — Capstone Clinic & Synthesis — Slide Deck

| Field | Value |
|---|---|
| Slides | 17 (120 min: 10 open · 40 clinic · 5 break · 55 synthesis drill · 10 wrap; final-exam briefing) |
| Companions | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) · [capstone rubric](../../assessments/rubrics/capstone-rubric.md) |
| Style | [Course deck conventions](../../lectures/README.md#deck-conventions) |

## Deck outline

| # | Slide | # | Slide |
|---|---|---|---|
| 1 | Title | 10 | Worked example: one flow, full stack |
| 2 | Hook: defend it in 15 minutes | 11 | The examiner's question bank |
| 3 | Capstone stage gates | 12 | Synthesis drill brief |
| 4 | Clinic: stage-1 design review | 13 | Classroom questions |
| 5 | The defense format | 14 | Common misconceptions |
| 6 | Explainability rule | 15 | Summary of the course |
| 7 | What "verification" means here | 16 | Final-exam briefing |
| 8 | Worked example: failover answer | 17 | Exit: the course in one packet |
| 9 | Defense rubric walk | | |

## Slides

### Slide 1 — Title
**Computer Networks — Lecture 32**
Capstone clinic & synthesis

> Notes — The last lecture: everyone defends, everyone synthesizes. The course ends by *using* everything.

### Slide 2 — Hook: defend it in 15 minutes
- Your design, your build, your dashboard — 15 minutes, then questions
- The questions don't care what worked; they ask *why* and *what if*
- Today practices exactly that hour

> Notes — 2 min. The defense is 15% of the capstone (rubric); today's clinic is the rehearsal. Names on the rotation board now.

### Slide 3 — Capstone stage gates

| Stage | Due | Weight |
|---|---|---|
| Design document | W13 | 25% |
| Build demo | W15 clinic | 20% |
| Dashboard + data | W16 | 20% |
| Final report | W16 | 20% |
| Defense (today = rehearsal) | W16 | 15% |

> Notes — The rubric's stage table verbatim (quiz W16 Q4's source). Peer factor ±10% announced once more, with the integrity doc's explainability rule.

### Slide 4 — Clinic: stage-1 design review
- Two teams present 5-minute design snapshots
- Class runs the examiner's questions (next slides)
- Instructor notes gaps against the stage-1 rubric rows

> Notes — 40 min clinic. The audience acts as examiners — the best rehearsal for their own defense. Rubric rows referenced by name, not shown in full.

### Slide 5 — The defense format
- 15 min: requirements → design → build → evidence → lessons
- Then per-member Q&A: one design question, one evidence question each
- "We don't know, here's how we'd find out" scores; bluffing doesn't

> Notes — The format is the rubric's defense stage (15%). The unknown-handling line is worth repeating twice — it changes student behavior.

### Slide 6 — Explainability rule
- Every listed member explains *any* part on demand
- Inability ≠ participation issue → integrity process
- Pairs/teams: this rule was on every brief since L20 — today it bites

> Notes — Read from the integrity doc §1 verbatim. This slide exists so no one is surprised in W16.

### Slide 7 — What "verification" means here
- Planned tests with pass criteria (L31's section 5)
- *Actually executed*, with real outputs in the report
- Failover, load, security — each demonstrated, not asserted

> Notes — The rubric's stage-2/3 rows demand this. "Executed with outputs" is the evidence-reproducibility rule (integrity doc §2) applied to teams.

### Slide 8 — Worked example: failover answer
- Examiner: "the core switch dies — what happens?"
- Weak: "we have redundancy" (assertion)
- Strong: "uplink fails over via STP-class logic; we measured 2.1 s convergence, 0 lost pings after; here's the recorded test"

> Notes — THE worked example (quiz W16 Q5's answer shape). The three-part answer: mechanism → measured number → artifact. Write the template on the board.

### Slide 9 — Defense rubric walk
- Presentation 5 · individual Q&A 8 · unknown-handling 2 (of 15 stage weight)
- Q&A grades the *individual* — the peer factor adjusts, not replaces
- The question bank: requirements, failure, capacity, security, monitoring

> Notes — Rubric stage-5 rows named; the full table prints in the worksheet. The five question families preview slide 11.

### Slide 10 — Worked example: one flow, full stack
- Staff laptop → `https://portal.internal.corp/` — narrate every layer *and* policy point
- DNS → gateway ARP → VLAN firewall → routing → TLS → app
- The course in ninety seconds

> Notes — Quiz W16 Q6 / review-M8 Q9's synthesis trace, delivered live. Students then do their own at the drill (slide 12).

### Slide 11 — The examiner's question bank

| Family | Sample question |
|---|---|
| Requirements | "why /26 here?" |
| Failure | "what dies when X dies?" |
| Capacity | "show the BDP math" |
| Security | "which control stops X?" |
| Monitoring | "what does your dashboard miss?" |

> Notes — The five families = the rubric's Q&A spread. Teams drill each against *their* design in the clinic.

### Slide 12 — Synthesis drill brief
- Pairs: trace one flow across all layers + policy points (own capstone or the Meridian campus)
- Then: answer two examiner questions from the bank, out loud
- 45 min rotating plenary — everyone speaks once

> Notes — The synthesis drill is the final's §E rehearsal *and* the defense rehearsal in one. "Everyone speaks once" is enforced by the rotation.

### Slide 13 — Classroom questions
1. Which design section answers "what dies when the core dies?"
2. Your monitoring stage shows green — what's your first examiner question to *yourself*?
3. Where do the DS tenants' RTT-bound workloads appear in your design?

> Notes — Q2: tails/percentiles (L29's lesson, now self-applied). Q3: addressing + capacity sections (L31's DS thread).

### Slide 14 — Common misconceptions
- "The demo *is* the defense" → evidence + reasoning carry the marks; demos show *what*, defense shows *why*
- "Verification = it worked once" → planned tests, pass criteria, recorded outputs
- "Individual marks don't exist in teams" → Q&A is individual; the peer factor adjusts ±10%

> Notes — The first misconception separates B-teams from A-teams; say it kindly but plainly.

### Slide 15 — Summary of the course
- L1–L4: what networks are, and how to *measure* claims
- L5–L16: the stack below IP and the addressing/routing machinery
- L17–L23: transport truth and application protocols
- L24–L32: security, operations, design — and defending all of it

> Notes — The four-arc recap (quiz W16 Q4's five-word version). Ask the class for the *one* idea they'd keep if they had to delete everything else — good last-lecture energy.

### Slide 16 — Final-exam briefing
- Cumulative, M4–8 emphasis; 120 min (proposed), 70 marks
- Format mirrors midterm + one synthesis question (§E)
- Formula sheet provided; sample = review sets M4–M8 + this lecture's drill

> Notes — 5 min logistics from [`assessments/exams/final-instructor.md`](../../assessments/exams/final-instructor.md) §post-exam notes. Point to review-m8's Q9 as the synthesis rehearsal.

### Slide 17 — Exit: the course in one packet
Write the journey of one HTTPS packet from a staff laptop to an internal server — every layer, every policy point, in order.
*(Then: go defend something you built.)*

> Notes — The final exit slip doubles as the synthesis rehearsal artifact. Collect; the strongest traces go back to next semester's L31 as (anonymized) exemplars.

### Demonstration instructions (instructor)
- Clinic logistics: rotation board, timer visible, rubric rows in the worksheet
- Defense rehearsal: the examiner script = slide 11's bank + rubric stage-5 rows — same script the real defense uses (fairness by rehearsal)
- No devices required; team design docs are paper for today

### References for the deck
- Capstone rubric: [`../../assessments/rubrics/capstone-rubric.md`](../../assessments/rubrics/capstone-rubric.md)
- Final exam package: [`../../assessments/exams/final-student.md`](../../assessments/exams/final-student.md)
- Review sets M1–M8 (sample-paper material)
