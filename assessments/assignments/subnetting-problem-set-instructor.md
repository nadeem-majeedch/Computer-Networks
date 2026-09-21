# Subnetting Problem Set — Instructor Key & Marking Scheme

| Field | Value |
|---|---|
| Access | Instructor only — do not distribute |
| Verification | All arithmetic below is **[MC]** — reproduced by `tools/scripts/verify_assessment_numbers.py` (subnet math via Python `ipaddress`) |
| Marking | Total 100: correctness 60 (per-task below) · justification 25 · hygiene 15 — per the brief and [`../marking-guide.md`](../marking-guide.md) §1–§3 |

## Task 1 — Masks and hosts (10)

(a) /26 → 62 · /27 → 30 · /28 → 14 (3). (b) 300 hosts → **/23** (510; /24 gives 254)
(4). (c) **/30** (2 usable) — accept /31 with RFC 3021 point-to-point note (3).

## Task 2 — Split and verify (10)

Eight equal /24s from 172.16.40.0/21 (2048 addresses): **172.16.40.0/24 through
172.16.47.0/24**; ranges .0–.255 per subnet; broadcast = x.x.x.255; mask
255.255.255.0 (6). Unused per subnet: **2 reserved addresses** (network + broadcast)
(4).

## Task 3 — VLSM plan (15)

Ordering rule must be stated (largest-first assumed below) (3). Allocation:

| Need | Prefix | Range (usable) |
|---|---|---|
| 400 | 10.150.0.0/23 | 10.150.0.1 – 10.150.1.254 |
| 120 | 10.150.2.0/25 | .2.1 – .2.126 |
| 60 | 10.150.2.128/26 | .2.129 – .2.190 |
| 20 | 10.150.2.192/27 | .2.193 – .2.222 |
| link 1 | 10.150.2.224/30 | .2.225 – .2.226 |
| link 2 | 10.150.2.228/30 | .2.229 – .2.230 |
| reserve /28 | 10.150.2.240/28 | .2.241 – .2.254 |

(9 for all ranges correct; −1 per error, floor 0). Free block: **10.150.2.232/29**
(8 addresses) — the /28's 16-alignment jumps over it (3). Teaching point: alignment
rules create fragments; mention in feedback.

## Task 4 — Membership and aggregation (10)

(a) 60-host subnet range .129–.190; 200 ∉ → **not inside** (range test shown) (5).
(b) Four contiguous /24s → **172.16.40.0/22**; safe only if no covered prefix is
routed/announced more specifically elsewhere (longest-prefix exception rule) (5).

## Task 5 — Growth plan (10)

380 × 1.25 = 475 (year 1) ≤ 510 ✓; × 1.25 = 594 (year 2) > 510 ✗ (4). Survives year 1
only; smallest prefix surviving the full horizon: **/22** (1 022) (3). The /22 must
ship **during year 1**, before the second compounding (3).

## Task 6 — Design defense (5)

Open answer. Full credit: clear position + two named concepts correctly applied
(e.g., flat /16 = one broadcast domain of 65k hosts — ARP/DHCP load and L2 attack
blast radius; aggregation still works with structured sub-allocation). Partial (3):
position + one concept. The *refute* position is easier to defend but *defend-with-
guardrails* (structured /24-per-VLAN inside the /16) also earns full credit.

## Justification marks (25)

Award across tasks 3–6: ordering/alignment rules stated (8) · trade-offs or
growth reasoning explicit (9) · correct use of course terminology (VLSM, usable,
alignment, longest prefix) (8).

## Hygiene marks (15)

Working shown for every numeric step (6) · assumptions section present (5) ·
document readable/organized (4).

## Common errors to annotate

- Confusing "usable" with "total" (off-by-two).
- Allocating 400 hosts a /24 (254 < 400) — check the boundary.
- Forgetting the /28 alignment jump in Task 3 (leads to "no free block").
- Task 5: comparing year-2 demand against the /23 without compounding both years.
