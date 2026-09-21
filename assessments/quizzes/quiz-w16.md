# Weekly Quiz — Week 16 (L31, L32) — synthesis week

| Field | Value |
|---|---|
| Coverage | L31 — Enterprise design & data-science connection · L32 — Capstone workshop & synthesis |
| Mode | Formative, ~12 min (design-flavored; serves as final-exam rehearsal for synthesis items), individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [I|CLO6|L31]** You must segment a 250-staff company into at least: staff, servers,
guests, and building-automation devices. State one subnetting *and* one firewall
principle you apply (names suffice).

**Q2 [I|CLO5|L31]** A data-science pipeline copies 200 GB nightly between two sites on
a 1 Gb/s link with 30 ms RTT. Ideal minimum transfer time, and which single factor
usually pushes real time far above it? (Show the division; you may state TCP-window
effects in words.)

**Q3 [I|CLO6|L31]** Your model-training job reads a dataset of 100 000 small files.
Which network behavior dominates — per-file latency or link bandwidth — and what
architectural change (name one) attacks the real bottleneck?

**Q4 [I|CLO6|L32]** Give the capstone's design-review spine in five words or fewer per
stage: requirements → addressing → switching/routing → services → verification.

**Q5 [A|CLO6|L32]** Defend in 3 sentences: why "it worked in the lab" is insufficient
evidence that an enterprise design is correct, and what artifact (one) from your
capstone closes most of that gap.

**Q6 [E|CLO8|L32]** Name one thing you would redesign in this course's network if
budget doubled, and the CLO-level evidence you would bring to justify it.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Subnetting principle: one subnet per role/site with headroom (VLSM, sum of
hosts + growth ≤ subnet size). Firewall principle: default-deny between zones with
explicit least-privilege permits (guests reach internet only; automation devices are
inbound-deny). Names + one clause each suffice. [I·CLO6]

**Q2.** 200 GB = 1.6×10¹² bits ÷ 10⁹ b/s = **1600 s ≈ 26.7 min** [MC]. Real time rises
mainly because TCP can't keep the pipe full (window vs 30 ms BDP ≈ 3.75 MB), plus
protocol overhead — accept window/BDP reasoning in words. [I·CLO5]

**Q3.** Per-file *latency* dominates: 100 000 × RTT-scale per-file round trips swamp a
1 Gb/s link. Architectural fix: pack files into larger objects/archives (fewer round
trips) or pipeline/parallelize transfers (any one, with the round-trip mechanism). [I·CLO6]

**Q4.** Requirements → **addressing plan** → **L2/L3 topology** → **services (DHCP/DNS/
routing policy)** → **verification (tests/measurements)**. Five stages named; wording
flexible. [I·CLO6]

**Q5.** Lab success shows *one* path under *benign* conditions; enterprise correctness
requires behavior under failure, load, and misconfiguration (convergence, failover,
capacity). Artifact: a verification/measurement report (tests actually executed:
failover test, load test, monitoring baseline) — accept monitoring dashboard with
recorded incident. [A·CLO6]

**Q6.** Open — credit requires a named change *and* evidence type tied to a CLO (e.g.,
"replace flat L2 with VLAN-per-floor: cite L09/L16 lab results + CS-03 RCA showing
broadcast-domain blast radius"). [E·CLO8]
