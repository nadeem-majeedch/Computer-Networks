# LAB-16 — Instructor Guide

## Setup (before session)
- Print the eight requirement cards (2 deliberately vague: "fast Wi-Fi", "secure servers")
  for T1's triage; write the Building C brief on the board.
- Prepare the failover demonstration (transcript route): down an uplink while pinging,
  record the outage window — students predict the window *before* seeing it.

## Solutions / expected values
- **Pre-lab 1:** requirements → hierarchy → address plan → policy; graded by stated
  justifications.
- **T1:** testable rewrites, e.g. "fast Wi-Fi" → "≥25 Mbit/s per user at p95 in 90% of
  floor area" (L30/L31 vocabulary).
- **T2:** Building C reference shape: staff 440→/23 (10.30.0.0/23), guests 120→/25,
  servers /24 carved into 3× /26-ish tiers, uplinks /30-ish or /31-note; summary 10.30.0.0/20
  (accept any exact-covering summary with proof).
- **T3:** the assertion script catching an overlap/headroom slip is the *expected* event
  for at least one pair per session — celebrate it as the method working.
- **T4:** guest isolation: guest ping to staff fails, guest ping to internet succeeds
  (NAT exists); failover: outage window ≈ ARP/convergence time, measurable in the ping log.

## Common failure modes
1. Designs "pass" T3 because the student fixed the assertion instead of the plan — compare
  against the handout script.
2. T4 scope creep (whole campus in 25 min) — hold to one slice; rubric rewards the honest
  demonstration of one property.
3. Defenses without evidence ("we would…") — the rubric's evidence discipline from L31/CS-04
  applies verbatim.

## Recognition grading (no course weight)
Findings page + defense quality; strongest designs feed the CS-04 exemplar pool (with
student permission) for next semester.
