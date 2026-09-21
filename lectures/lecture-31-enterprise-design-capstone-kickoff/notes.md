# Lecture 31 — Instructor Teaching Notes
## Enterprise Design & the Data-Science Connection (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO6 primary; CLO4/CLO7 integration |
| Textbook anchor | PD design sections revisited; CS-04 brief (authoritative for kickoff) |

---

## 1. Objectives hook
Board: **"Everything since L01 converges today: one building, one address
plan, one policy — designed, defended, and reviewed."**

Hook (2 min): the Meridian Systems campus map (CS-01's artifact) enlarged —
"by 11:50 you'll have critiqued a design for this company, and by next week
yours will be the one on the screen."

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | Semester map; Meridian map reveal |
| 6–24 | Concept 1 | The design method: requirements → hierarchy → address plan → policy |
| 24–38 | Worked example | Instructor designs Meridian's Building A live (think-aloud) |
| 38–42 | CS-04 kickoff briefing | Deliverables, roles, timeline |
| 42–63 | Design clinic 1 | Teams draft their own design (address plan + VLAN map) |
| 63–68 | Break | — |
| 68–92 | Gallery walk + review | Teams post designs; structured peer review with rubric |
| 92–99 | Design clinic 2 | Teams revise from review evidence |
| 99–109 | The data-science connection | §3.4: classification, anomaly framing, forecasting, bias |
| 109–116 | Spotlights | Two teams defend one choice each |
| 116–120 | Summary + exit ticket | — |

## 3. Concept walkthrough

### 3.1 The design method (18 min)
- **Step 1 — Requirements:** users/devices per site, growth %, applications
  (VoIP? video?), security zones, budget/complexity tolerance — write them
  as testable statements; vague requirements make ungradeable designs.
- **Step 2 — Hierarchy:** core/distribution/access (the classic 3-tier),
  collapsed-core for small sites; each layer's job named (CLO6 vocabulary
  the rubric will grade).
- **Step 3 — Address plan:** VLSM from L13, growth headroom policy
  (doubling or +20% — *state* the rule), VLAN map (L09) with purpose per
  VLAN; department-per-VLAN vs function-per-VLAN trade-off named.
- **Step 4 — Policy & zones:** user/guest/server/management zones (L25's
  blast-radius language); NAT edge (L14); redundancy choices and their
  failure scenarios.
- **The discipline:** every choice gets a *because* — the design review
  rubric grades justifications, not diagrams alone.

### 3.2 Worked example — think-aloud (14 min)
Instructor designs Building A live: 180 staff + 40 guests → VLANs 10/20/99;
VLSM from 10.20.0.0/16 (state the headroom rule aloud, choose +growth);
uplinks sized from measured traffic (L29's numbers, cited); guest zone
policy copied from L25's lab. Students capture the *why* for each step —
the think-aloud models exactly what CS-04's written defense requires.

### 3.3 CS-04 kickoff (4 min briefing)
- **Deliverables:** design document (with the four steps as sections),
  working prototype (from GA/LAB builds), evidence bundle, 10-minute
  defense.
- **Roles:** lead designer, implementation lead, evidence/ops lead —
  rotation permitted once; the rubric grades both the artifact and the
  defense.
- **Timeline:** kickoff today → prototype by next lecture → defense in
  L32's clinic slot; the CS-04 brief is authoritative.

### Reference diagram — Three-tier campus hierarchy

```text
                 ┌──────────────────────┐
                 │ core (L3, redundant) │
                 └───┬───────┬───────┬──┘
              ┌──────┘       │       └──────┐
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │    dist  │   │    dist  │   │    dist  │
        └──┬────┬──┘   └────┬─────┘   └──┬────┬──┘
      access access    access       access  access ── hosts
```

### 3.4 The data-science connection (10 min)
- **Traffic classification:** flows as feature vectors (sizes,
  inter-arrival times, ports) → supervised models can sort apps; the
  design implication: classification needs *measurement points* —
  place them in the design on purpose.
- **Anomaly detection framing:** L29's baselines become training data;
  anomalies are deviations — the design supplies clean vantage points.
- **Capacity forecasting:** L29's p95 time series forecast growth; the
  headroom rule (Step 3) is the design's answer to a forecast.
- **Measurement bias & ethics:** sampled flow records skew toward big
  flows; user-behavior telemetry has privacy implications — say what
  you collect and why (the week-1 ethics gate, come full circle).

## 4. Important definitions
Requirements statement · Hierarchy (core/distribution/access, collapsed
core) · Address plan (VLSM + headroom rule) · VLAN map · Security zone ·
Blast radius · Redundancy (named shapes) · Design review rubric ·
Justification discipline ("every choice gets a because").

## 5. Real-world examples
- **The failed audit story:** a mid-size campus with no VLAN map and /24s
  sprayed per switch — the design method exists because this is common.
- **CS-01→CS-04 arc:** the same Meridian requirements, now answered by the
  students instead of revealed to them — the semester's payoff.

## 6. Mathematical/technical example
VLSM headroom arithmetic (from the think-aloud): 180 staff devices → /24
(254 usable) with 2× headroom policy for growth; 40 guests → /26 (62) with
the same rule; aggregate check against the /16 campus block and route-summarization
opportunity to the core (L16's summary-route idea, applied to the plan).

**Latency- vs bandwidth-bound transfers (DS sizing):** 10,000 × 50 KB
files at 20 ms RTT take ≈ 200 s even with *infinite* bandwidth when
serialized — parallelism and batching are the levers; forecast link
sizes only after naming which regime the workload lives in.

## 7. Design clinic mechanics (46 min total)
Clinic 1 (21 min): teams receive the CS-04 brief + blank design template;
produce address plan + VLAN map + one-paragraph zone policy. Gallery walk
(24 min): designs posted; reviewers use the 4-point rubric (requirements
met? headroom stated? zones defensible? blast radius considered?) — each
reviewer writes *evidence*, not adjectives. Clinic 2 (12 min): revise from
evidence. ⚠ Print briefs/templates; the rubric in the worksheet is the
review instrument — keep timing strict, the gallery walk eats time.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Good design = biggest budget" | Trade-off discipline beats spend; rubric grades justification |
| "One flat network is simpler, therefore better" | Blast radius; the guest/management zone stories refute it |
| "VLANs by department, always" | Function-per-VLAN often scales better; state the rule you chose |
| "Redundancy always helps" | Each redundancy adds failure modes; justify per requirement |
| "The design document is the drawing" | The *defense* is graded — every choice needs its because |

## 9. Suggested practical demonstration
The gallery walk itself is the demonstration; if a spare screen exists,
display last year's (anonymized, ⚠ if available) design vs its post-mortem.
Fallback: the think-aloud slides.

## 10. Classroom activities
- **Requirements triage:** 8 requirement statements, teams rewrite the vague
  ones as testable claims (models Step 1 before the clinic).
- **Blast-radius sketch:** pick a zone boundary; enumerate what breaks if
  that zone is compromised — the CLO6 evaluation habit, rehearsed.

## 11. Problem-solving questions
1. 120 staff / 25 guests / 12 servers: propose VLAN counts + CIDRs with a
   stated headroom rule.
2. Your collapsed-core link carries 900 Mbps of 1 Gbps at p95 (L29 data).
   Name two design responses and their trade-offs.
3. Guest Wi-Fi must not reach staff VLANs but needs internet: which two
   constructs implement it, and where does the NAT happen?
4. A design has no management VLAN. Argue the risk in blast-radius terms.
5. Growth doubles Building B in 18 months: which plan choice absorbs it
   without renumbering, and why?

## 12. Formative assessment (with answers)
- MCQ: Headroom policy is stated so that → reviewers can check the plan
  (gradeability, not decoration).
- MCQ: Collapsed core suits → small sites with limited growth.
- Short: one requirement → testable rewrite ("fast Wi-Fi" → "≥ 25 Mbps per
  user at p95 in 90% of floor area" — accept equivalents).
- Exit diagnostic: zone boundary sketch with blast-radius label.

## 13. Exit ticket
1. The four design steps in order: ________
2. Your headroom rule and why: ________
3. One thing you'll change in your CS-04 design after the review: ________

## 14. Anticipated difficulties
- Time: the gallery walk must be capped (timer visible) or the clinic dies —
  the notes' minute plan is deliberately strict here.
- Teams may design "everything at once"; the template's section order
  enforces the method — hold them to it.

## 15. Instructor preparation checklist
- [ ] ⚠ Print CS-04 briefs, design templates, rubrics (1 per team + spare)
- [ ] Board pre-write: 4-step method; Meridian map; rubric summary
- [ ] Think-aloud slides ready; gallery-walk wall space arranged
- [ ] Teams pre-assigned (or a fast formation plan); timer visible

## 16. Timing fallbacks
Spotlights may drop (gallery evidence already covers CLO6 evaluation);
Clinic 2 may compress to a revision list (revise before L32); the worked
example can shorten by pre-drawing the map.

## 17. References
- PD design sections revisited; CS-04 brief (authoritative); the course's
  own L09/L13/L14/L16/L25/L27 notes (the design method cites them).
- Meridian artifacts from CS-01; ⚠ anonymized past designs if available.
