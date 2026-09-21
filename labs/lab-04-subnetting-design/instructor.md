# LAB-04 — Instructor Guide

## Setup (before session)
- No lab infrastructure needed; ensure every student has Python 3 available (any machine).
- Keep the `ipaddress` snippets on the course share for the verification step.

## Answer key (drills — verify before teaching this; numbers re-derived with `ipaddress`)
1. 192.0.2.0/24 → .0/26, .64/26, .128/26, .192/26; each: 62 usable, broadcast = next-1.
2. 172.16.9.0/24 largest-first: 60→.0/26 (62 ok), 30→.64/27 (30 ok), 12→.96/28 (14 ok),
   2→.112/30 (2 ok). Waste check: no overlaps; .116+.119 etc. remain for growth.
3. 10.20.4.96/27: network .96, broadcast .127, usable .97–.126; 10.20.4.110 ∈ yes.
4. 192.0.2.137/26 → 192.0.2.128/26 (usable .129–.190). Gateway convention: accept any
   *stated* convention (first usable is common) — the discipline is stating it.
5. 192.0.2.0/25 summarizes the two /26s (they are adjacent halves of it).

## Design exercise (T2) — one worked solution to grade against
Headroom ×2: staff 360→/23 too big, /24 (254) insufficient, so /23? — rubric accepts either
*stated* rule consistently applied; largest-first VLSM within 10.20.0.0/16, e.g.:
staff 10.20.0.0/23 (510 ≥ 360), guests 10.20.2.0/24 (254 ≥ 80), printers 10.20.3.0/26,
servers 6 × /26 from 10.20.4.0/24, p2p reserve 10.20.8.0/22 (/30s). Summary to core:
10.20.0.0/20 (if the above used the first 4k) — accept any *correct* summary that covers
exactly the used space; require the assertion snippet as proof (T3).
⚠ Grade the method (rule stated, order correct, no overlap, summary exact), not this
particular layout.

## Verification snippets (what T3 output should look like)
- `ipaddress.ip_network("10.20.0.0/23").subnet` checks; overlap test via
  `a.overlaps(b)`; summary check: `ipaddress.ip_network("10.20.0.0/20") in
  ipaddress.ip_network("10.20.0.0/16")` plus coverage assertion over the table.

## Common failure modes
1. Drill 2 done smallest-first → overlap at .96/.112 — use it as the teaching moment
   post-lab 1 asks for.
2. Headroom rule applied inconsistently (doubled printers but not servers) — rubric
   deducts under "correct results", not clarity.
3. Summary route off by a non-power-of-two → assertion fails; students "fix" the
   assertion instead of the plan. Watch for edited assertions (compare with the handout).

## Grading notes (5% instrument)
- Grade per-drill correctness (40%), design method (40%), T3 verification honesty (20%).
- Due L16 per the schedule; the due-date line in the schedule is authoritative.
- The IPv6 challenge is recognition-only (consistent with the workbook policy).
