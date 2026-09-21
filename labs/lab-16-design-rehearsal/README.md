# LAB-16 — Network Design Rehearsal (optional, recognition-only)

| Field | Value |
|---|---|
| Anchor lectures | L31 (enterprise design + DS connection), L32 (capstone clinic); CS-04 brief |
| CLOs | CLO3, CLO6, CLO8 |
| Assessment | **Optional — recognition only, zero course weight** ([`../syllabus-safety.md`](../syllabus-safety.md) §2) |
| Mode / duration | Pairs or solo; 2-h session + 48-h window |
| Environment | Paper + lab namespaces for the verification sprint; `ip`/Python `ipaddress` |

## Learning outcomes
1. Run the full L31 design method under time pressure: requirements → hierarchy →
   address plan → policy, with every choice carrying a *because*.
2. Verify your own design's arithmetic (no overlaps, correct summary, headroom honored)
   programmatically — the design is only as good as its check.
3. Prototype one slice of the design in namespaces (a mini three-tier or a VPN'd pair of
   segments) and demonstrate the failure mode you claimed to defend against.
4. Defend the design in a 5-minute peer review using the CS-04 rubric's shape.

## Pre-lab
1. L31's four design steps, in order — and the discipline that grades them.
2. Your headroom rule (LAB-04's habit): state it; you will apply it under time pressure.
3. One failure mode your CS-04 design claims to survive — bring it; you will *test* it.

## Tasks

### T1 — Requirements triage (15 min)
Eight requirement cards (course share; e.g., "guests isolated", "server growth ×2",
"management reachable only from NOC", "voice VLAN"): rewrite the vague ones as testable
statements. Your design grades against your own rewrites.

### T2 — Design sprint (35 min)
Meridian Building C (new brief): 220 staff, 60 guests, 14 servers in 3 tiers, 2 uplinks.
Produce: hierarchy sketch, VLAN map, VLSM table (headroom rule applied), zone policy
one-paragraph, and the summary route to the core. Hand-arithmetic first, then:

### T3 — Programmatic verification (15 min)
```python
import ipaddress
plan = [("staff", "10.30.0.0/23"), ("guests", "10.30.2.0/24"), ...]
nets = [ipaddress.ip_network(c) for _, c in plan]
assert all(not a.overlaps(b) for i, a in enumerate(nets) for b in nets[i+1:])
# summary check: smallest supernet containing all == your claimed summary
```
Include the script + output. **A design that fails its own check is a finding, not a
failure** — fix and re-run, keep both outputs.
**Expected observation:** the verification script matches your hand arithmetic exactly
when the plan is right; any mismatch means the *plan* moved, not the script.

### T4 — Prototype one slice (25 min)
Namespaces: implement the guest-isolation slice or the two-uplink failover slice (link
down test with `ip link set down`) — demonstrate the property you claimed. Capture the
evidence (command output + one line of interpretation). Small is fine; *honest* is
mandatory.

### T5 — Peer defense (20 min)
5-minute CS-04-shaped defense per design: requirements met? zones defensible? failure
mode actually tested? Reviewers score with the rubric's evidence discipline (write
evidence, not adjectives).

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Overlap assertion fires | VLSM order or headroom slip | largest-first re-derivation; keep the failing output |
| Failover test "passes" trivially | ping never stopped (wrong target) | down the *right* link; watch the ping's outage window |
| Defense runs out of time | defending everything | pick the two strongest choices; depth beats breadth |

## Post-lab questions (findings page)
1. The requirement you *rejected* as untestable, and the testable rewrite you negotiated.
2. Your T3 verification: what did the machine catch that your eyes missed?
3. Your prototype's demonstration: the property, the test, the evidence — and what it
   does *not* prove.
4. Which CS-04 rubric dimension is your design currently weakest on, and your fix plan.

## Challenge (ungraded)
IPv6 side-plan: /64 per VLAN under 2001:db8:acad::/48, nibble-aligned, with the same
verification script pattern. (RFC 8374 documentation range; cite it.)

## Accessibility / low-resource alternatives
- T1–T3, T5 are fully paper/text; T4 has a transcript-based alternative (provided
  failover demonstration + your written prediction before it plays out).
- Remote pairs: peer defense over any call; rubric sheet unchanged.

## Safety notes
Namespaces only; fault injection on your own build (syllabus-safety §3.7).
