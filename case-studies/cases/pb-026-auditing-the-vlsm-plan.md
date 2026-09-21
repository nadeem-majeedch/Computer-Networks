# PB-026 — Auditing the VLSM Plan (L13, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L13 — IPv4 Subnetting & VLSM |
| CLOs | CLO5 (VLSM computation), CLO6 (design review) |
| In-class slot | Main activity; 25 min, pairs |
| Case type | Design review + calculation · Topic: Subnetting/VLSM |
| Evidence policy | Synthetic plan, labeled; every claimed error is arithmetically demonstrable |

---

## Student version

### Scenario
Meridian opens a third floor. The intern produced a VLSM allocation from
`10.20.96.0/19` for four departments. Your job: audit it *before* the change window.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Available block:  10.20.96.0/19   (8,192 addresses)
Requirements:
  Floor staff    ≤ 500 hosts      → intern assigned 10.20.96.0/23
  Lab machines   ≤ 250 hosts      → intern assigned 10.20.97.0/24
  IoT sensors    ≤ 60 hosts       → intern assigned 10.20.98.0/26
  Printers       ≤ 30 hosts       → intern assigned 10.20.98.64/29
  (growth note: floor staff expected to double within 18 months)
```

### Problem statement
Audit each assignment: is the prefix large enough, do any allocations overlap, and is
there room for the stated growth? Produce a corrected plan if needed, allocated
efficiently (largest first).

### Evidence pack
The labeled synthetic plan. All judgments are pure arithmetic on the given numbers —
no platform behavior involved.

### Constraints
- Show the size check for each line (usable hosts vs requirement).
- Check pairwise overlaps explicitly.
- If you correct the plan, keep it inside 10.20.96.0/19 and preserve the /23-then-/24
  ordering efficiency.

### Student questions
1. Size-check each of the four assignments (usable hosts vs requirement).
2. Which two assignments overlap? Show the ranges.
3. The growth note: which single assignment is already too small for 18 months out?
4. Produce the corrected plan (largest first) and state how many addresses remain
   unallocated.

### Expected learning outcomes
- Convert prefix length to usable host counts and validate requirements.
- Detect overlapping allocations by range arithmetic.
- Produce a clean VLSM plan with explicit headroom accounting.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Usable hosts = 2^(32−prefix) − 2. Do each line before you judge it."
2. "Two lines both claim space starting at 10.20.98.0. Draw the ranges."

### Solution
1. Size checks: /23 → 2^9−2 = 510 ≥ 500 ✓. /24 → 254 ≥ 250 ✓. /26 → 62 ≥ 60 ✓.
   /29 → 6 < 30 ✗ (printers need /27 = 30 usable ✓ exactly, or /26 for headroom).
2. Overlap: staff 10.20.96.0/23 spans **10.20.96.0–10.20.97.255**. Lab
   10.20.97.0/24 spans 10.20.97.0–10.20.97.255 — **fully inside the staff range**.
   Also IoT 10.20.98.0/26 (98.0–98.63) and printers 10.20.98.64/29 (98.64–98.71) don't
   overlap each other — the only collision is staff×lab.
3. Growth: staff 500→1000 hosts needs >1022 ⇒ a /22 (1022 usable) minimum; the /23 is
   already too small for the stated horizon.
4. Corrected plan (largest first, from 10.20.96.0/19):
   - Floor staff: 10.20.96.0/**22** (96.0–99.255, 1022 usable ✓ growth ✓)
   - Lab machines: 10.20.100.0/**24** (254 ✓)
   - IoT sensors: 10.20.101.0/**26** (62 ✓)
   - Printers: 10.20.101.64/**27** (30 ✓, tight — flag one-tier-up option /26 for
     spares: then IoT must move; note the trade-off)
   - Remaining unallocated: block covers 96.0–103.255; used through 101.95 ⇒ free
     range 101.96–103.255 = (101.96→101.255: 160) + (102.x: 256) + (103.x: 256) =
     **672 addresses**.
   Teaching note: requiring students to *show the subtraction* is the point — the
   "remaining" figure is where most audits go wrong.

### Reasoning process
Facts: requirements, block, four prefixes. Model: usable = 2^h − 2; ranges by network/
broadcast arithmetic; overlap = intersection non-empty. Rebuild largest-first with
explicit headroom; account leftover space.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| 2^(32−prefix) without −2 | Network/broadcast aren't hosts; /26 "64" vs 62 matters at the boundary (60 ≤ 62 but 62 ≤ 64 flatters printers) |
| Checking size only | The intern's fatal error was overlap; size checks alone would pass three lines |
| Allocating smallest first | Fragments the block; large future needs won't fit contiguously |
| "Enough for today" growth math | The /23 fails the *stated* 18-month requirement — an audit must check the horizon given |

### Extension question
Finance asks for the *minimum* block that still satisfies everything including growth,
starting fresh. Derive it: largest-first contiguous need = /22 + /24 + /26 + /27 =
1024+256+64+32 = 1,376 addresses ⇒ what smallest power-of-two-aligned block fits
(1,376 → 2,048 = /21) — and show the allocation inside it. (10.20.96.0/21: staff
.0/22, lab 100.0/24, IoT 101.0/26, printers 101.64/27, leftover 101.96–103.255.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All four size checks with arithmetic; overlap ranges shown; growth-driven resize; corrected plan + exact leftover count |
| 3 Proficient | Finds overlap and printer error; leftover miscounted |
| 2 Developing | Checks sizes only; misses overlap and growth |
| 1 Beginning | "Looks fine" |

### References
- PD §4.3 (CIDR, subnetting arithmetic) ⚠ verify section mapping
- Kurose & Ross §4.3.4 (CIDR); VLSM practice per lecture L13 notes
