# LAB-07 — Instructor Guide

## Setup (before session)
- Test the full T0 script; it is the longest build in the workbook. Ship it as
  `lab07-build.sh` on the course share to save 15 minutes if session timing slips.
- Pre-capture `lab07-tr.pcapng` (offline route) from your own run.

## Solutions / expected values
- **Pre-lab 1:** `net.ipv4.ip_forward=1`.
- **Pre-lab 2:** ICMP time-exceeded (type 11); the probe's TTL (1, then 2, …).
- **Pre-lab 3:** 10.1.0.0/16 via B — longest prefix wins.
- **T1:** R2's entries: `10.0.12.0/24 dev r12b proto kernel scope link src 10.0.12.2` and
  `10.0.23.0/24 dev r23a ...` — connected routes cover everything it needs.
- **T2:** decrement happens at each forwarding hop (R1's egress side onward). On r12a
  (R1→R2 wire) requests show TTL 63; on the reverse direction replies carry 63→R1→62 to
  hostA (record actual numbers; capture-side subtlety is the discussion, see README).
- **T3:** probe TTL 1 → time-exceeded src 10.0.1.1; TTL 2 → src 10.0.12.2; TTL 3 reaches
  hostB → traceroute stops on reaching the target (three probes/hop; completion = reaching
  the destination, ICMP port-unreachable in UDP variants).
- **T4:** `ip route get` prints the /32; risk: stale/erroneous more-specifics blackhole
  traffic while everything else looks fine (the classic "one host unreachable" ticket).

## Common failure modes
1. Forgetting R3's return route (ping out, replies die) — the fix is half the learning;
   do not pre-fix it in the build script.
2. Students report traceroute hop count without the TTL→time-exceeded mapping —
   analysis rubric requires the mechanism.
3. `ip route get` confusion: it prints a *decision*, it does not send traffic — worth 30 s.

## Grading notes
- Correct results (40): T1 pattern + T3 probe/TTL/source table.
- Analysis (30): post-lab 2 (what changes with two /25s: R1 needs both specifics or a
  covering /23) and post-lab 4's risk statement.
- Reproducibility (20): predictions written *before* results (worksheet has the field).
- Challenge (asymmetric traceroute) frequently surprises — strong recognition candidates.
