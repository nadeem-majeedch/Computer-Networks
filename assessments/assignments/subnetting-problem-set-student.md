# Subnetting Problem Set — Student Brief

| Field | Value |
|---|---|
| Instrument | Individual assignment · **5% of course weight (proposed plan)** — see [`../README.md`](../README.md) §4 |
| Released / due | Released L13 · due L16 (start of lecture) |
| Weighting inside | Correctness 60% · design justification 25% · documentation hygiene 15% |
| Integrity | Strictly individual ([`../academic-integrity.md`](../academic-integrity.md) §1); state all assumptions |
| Format | One PDF or Markdown document; show working for every numeric answer |

## Instructions

Answer all six tasks. Where a task says *design*, justify choices in 1–3 sentences —
an unexplained correct number earns the correctness marks only. VLSM allocations must
state your ordering rule. Verify your own arithmetic before submission (a `python3`
`ipaddress` check or a calculator is fine); you do not submit the check, only the
result.

### Task 1 — Masks and hosts (10 marks)
(a) Usable hosts in /26, /27, /28. (b) Smallest prefix for 300 hosts. (c) Smallest
prefix for a point-to-point link under the course's conventions.

### Task 2 — Split and verify (10 marks)
Split 172.16.40.0/21 into eight equal subnets. Give each range, broadcast, and the
mask in dotted-decimal. State how many addresses remain unused *per subnet*.

### Task 3 — VLSM plan (15 marks)
From 10.150.0.0/22 allocate, in one plan: 400, 120, 60, 20 hosts; two /30 links; one
/28 future reserve. Give every prefix, range, and the free block left over. State your
ordering rule.

### Task 4 — Membership and aggregation (10 marks)
(a) Is 10.150.3.200 inside your Task-3 60-host subnet? Show the range test.
(b) Summarize 172.16.40.0/24 … 172.16.43.0/24 into one prefix, and state the condition
that makes the summary safe.

### Task 5 — Growth plan (10 marks)
A /23 serves 380 devices growing 25%/year for 2 years. Does it survive? Give the
smallest surviving prefix and the year the change must ship.

### Task 6 — Design defense (5 marks)
A colleague proposes putting *all* VLANs into one /16 "to avoid running out."
Write 3–5 sentences defending or refuting the proposal using two course concepts
(broadcast domain size, route aggregation — or your own).

---

**Submission checklist:** every numeric answer shows working · assumptions stated ·
ordering rules stated · no fabricated tool output (screenshots not required for this
assignment).
