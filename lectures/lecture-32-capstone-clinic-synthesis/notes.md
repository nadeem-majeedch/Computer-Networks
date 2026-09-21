# Lecture 32 — Instructor Teaching Notes
## Capstone Workshop, Presentations & Course Synthesis (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO8 primary (synthesis); CLO4/CLO6/CLO7 via CS-04 |
| Textbook anchor | CS-04 brief; student design documents |

---

## 1. Objectives hook
Board: **"Lecture 1 asked what a network is. Today your answer is a working
one, and you'll defend it."**

Hook (2 min): the L01 whiteboard photo (or redrawn "network web") beside the
room — teams' prototypes running on the benches. The arc's closing image.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–5 | Recap + hook | The arc; defenses' rules (10 min each, strict) |
| 5–60 | CS-04 defenses 1 | Teams defend prototype + design to rubric |
| 60–65 | Break | — |
| 65–90 | CS-04 defenses 2 | Remaining teams defend |
| 90–105 | Synthesis clinic | Teams build the playbook (worksheet Part B) |
| 105–114 | Playbook highlights | 3 teams read one playbook entry each |
| 114–120 | Synthesis map + exam guidance + exit ticket | The complete packet journey; what the exam looks like |

*(6 teams × 10 min = 60 min of defenses — ⚠ adjust team count/timing to
enrollment; with >6 teams move some defenses to a lab slot and protect at
least 40 min for the synthesis clinic.)*

## 3. Concept walkthrough

### 3.1 Running the defenses (55 min)
- **Format:** 10 min per team — 5 min demo/walkthrough, 5 min questions from
  the rubric (requirements met? zones real? operations evidence? failure
  handling?).
- **Evidence discipline:** every claim points at the artifact (screenshot,
  probe output, dashboard row from L29's build) — "we think" scores less
  than "we measured."
- **Failure question (the rubric's favorite):** instructor injects one
  scenario per team ("your DNS dies," "a rogue device appears") — teams
  reason live from their design's blast-radius claims (L31).
- **Scoring:** rubric in the worksheet is the record; write evidence, not
  adjectives — same discipline the gallery walk taught.

### 3.2 The synthesis clinic (15 min)
- **Playbook build (worksheet Part B):** each student writes — (1) their
  5-step troubleshooting loop with the layer each step interrogates;
  (2) three "if X, check Y first" rules harvested from the course
  (e.g., "new device silent → ARP/link first"; "slow only at 3 p.m. →
  utilization window"); (3) one design principle they'd defend in a job
  interview.
- **Why:** CLO8's synthesis is personal, not recited — the playbook is the
  take-home artifact; it doubles as the course's pedagogical audit trail.

### 3.3 Course close (6 min)
- The 8 modules as one sentence each — the map, walked once more.
- What comes next: OS/DC/networking electives, CCNA-adjacent *self*-study
  (the course deliberately isn't vendor cert-driven — say so), and the
  capstone showcase date.

### Reference diagram — The troubleshooting loop

```text
observe ──→ localize (which layer?) ──→ hypothesize ──→ test
    ▲                                                      │
    └────────────── fix / verify ←─────────────────────────┘
```

### 3.4 Synthesis map & exam guidance (inside the close)
- **The one-packet journey, complete:** walk L03's journey across the
  module map one final time — every hop now carries its lecture's
  vocabulary. This *is* the course-wide synthesis diagram.
- **Exam guidance:** coverage follows the assessment map (all 8 CLOs);
  expect scenario questions in rubric language ("identify, compute,
  defend"), packet-trace readings like the GAs, and design defense
  like today's — not vendor-trivia recall.

## 4. Important definitions
Defense rubric · Evidence discipline · Blast-radius defense (live) ·
Synthesis playbook · Troubleshooting loop (personal edition) · Design
principle (personal edition).

## 5. Real-world examples
- **The defense = a design review** — the exact ritual graduates will face
  in industry; the rubric's "failure question" is why interviewers hand
  candidates outages.

## 6. Mathematical/technical example
Rubric arithmetic: 5 rubric dimensions × 4 evidence points = 20; a team
claiming "secure zones" without a probe demonstrating isolation earns 0 on
that dimension regardless of diagram quality — the arithmetic of evidence.

## 7. Clinic mechanics (90 min total)
⚠ Team count/timing must be fixed **before** the lecture (enrollment-
dependent); the minute plan assumes 6 teams. Defenses run to the clock —
a visible timer and a 1-minute warning; the synthesis clinic is protected
time (CLO8 cannot be made up in reading). Backup plan if a prototype
fails live: walk the design document + evidence bundle (the rubric's
evidence dimension still scores).

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "A polished diagram is the capstone" | The prototype + evidence is; diagrams document |
| "Defense means reading the document aloud" | Q&A on failure scenarios; reading scores nothing |
| "Synthesis = listing the modules" | The playbook is personal rules, not a table of contents |
| "The course ends the learning" | Named next steps; vendor cert as self-study, not identity |

## 9. Suggested practical demonstration
The defenses themselves; plus instructor's closing 2-minute "one-packet
journey" recap on the room's own projected network (L03's packet journey,
now fully annotated by 32 lectures of vocabulary).

## 10. Classroom activities
- **Failure-question jar:** scenarios drawn per team — keeps the Q&A honest
  and unpredictable (the rubric's evidence dimension feeds on it).
- **Playbook swap:** two students exchange playbooks and mark one rule they
  would steal — synthesis made social.

## 11. Problem-solving questions (for spare minutes / lab slot)
1. Your capstone's private zone can reach the internet but guests can't
   reach it — walk which rule does that.
2. p95 latency doubles only during backups: which L29 instruments
   localize it?
3. A new device appears on the staff VLAN uninvited: first two probes?
4. Rename one course claim you'd now *revise*, with evidence — bonus for
   naming the lecture that changed your mind.

## 12. Formative assessment (with answers)
- The defense rubric **is** the formative assessment (written evidence per
  dimension; same sheet returned as summative record).
- Spot check during clinic: ask two students to name their playbook's
  first "check Y first" rule — coherence check for CLO8.

## 13. Exit ticket
1. My 5-step troubleshooting loop: ________
2. My favorite "if X, check Y first" rule: ________
3. One design principle I'd defend in an interview: ________

## 14. Anticipated difficulties
- Time: 10-minute defenses slip; the timer + 1-minute warning is not
  optional. Overflow teams → lab slot (decided by team count in advance).
- Prototype failures on the day: the backup plan (document + evidence walk)
  keeps the rubric scoreable without punishing bad luck alone.

## 15. Instructor preparation checklist
- [ ] ⚠ Fix team count/timing to enrollment; defense schedule printed
- [ ] Rubric sheets (1 per team + instructor copy); failure-question jar
- [ ] Benches/power for prototypes; spare adapters; test each team's demo
      slot assignment the day before ⚠
- [ ] L01 hook artifact ready (photo or redrawn web); course-close slides

## 16. Timing fallbacks
Playbook highlights may drop to two entries; the close may compress to the
8-module sentence map; defenses may not — if enrollment forces it, move
overflow to the lab slot rather than gutting the synthesis clinic.

## 17. References
- CS-04 brief (authoritative for rubric/deliverables); student design
  documents; the course's module notes (cited per defense claim).
- L31 notes for rubric lineage; GA-29/LAB-14 builds for evidence formats.
