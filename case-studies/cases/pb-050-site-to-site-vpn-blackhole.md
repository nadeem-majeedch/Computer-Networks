# PB-050 — The Tunnel Is Up, But Half the Building Is Dark (L25, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L25 — Perimeter & Internal Defenses: Firewalls, Segmentation, VPNs |
| CLOs | CLO3 (VPN selectors/tunnel semantics), CLO6 (diagnose partial-path faults) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: VPN/segmentation |
| Evidence policy | Synthetic configs/logs, labeled; selector behavior per IPsec policy model, vendor syntax flagged |

---

## Student version

### Scenario
The new site-to-site VPN between HQ-A and the co-lo facility came up green: phase 1
and phase 2 both established, tunnel counters incrementing. Yet only *some* traffic
crosses. The co-lo has two subnets; HQ has three.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (vendor-neutral syntax, illustrative):**

```
HQ-A subnets:   10.20.30.0/24 (staff), 10.20.40.0/24 (analytics), 10.20.50.0/24 (mgmt)
Co-lo subnets:  10.30.10.0/24 (compute), 10.30.20.0/24 (storage)
VPN phase-2 "traffic selectors" (both ends, symmetric):
  HQ-A side:   10.20.40.0/24 ↔ 10.30.10.0/24
  Co-lo side:  10.30.10.0/24 ↔ 10.20.40.0/24
Tests from HQ-A:
  analytics (10.20.40.5) → compute (10.30.10.7):   WORKS (ping + TCP)
  staff     (10.20.30.9) → compute (10.30.10.7):   fails (timeout)
  mgmt      (10.20.50.4) → storage (10.30.20.8):   fails (timeout)
Tunnel stats: encrypt counter rises only during analytics tests
Routes: both ends have routes for the remote /24s via the tunnel interface (all five)
```

### Problem statement
Explain why routing alone doesn't decide what crosses the tunnel (selectors vs routes),
account for *each* failing test, and produce the corrected selector set — plus the
design question the team should answer before adding more subnets.

### Evidence pack
The labeled synthetic configs. Facts: selectors list exactly one pair; routes exist
for all five subnets; encrypt counters track the working pair only.

### Constraints
- Explain routes-vs-selectors as two independent gates (what each answers).
- Corrected selectors must be explicit pairs; wildcards are a choice to justify, not
  a default.

### Student questions
1. Two gates decide whether a packet enters the tunnel. What does each gate ask?
2. Why does the staff→compute test fail *despite* correct routing? Trace the packet's
   decision at the HQ-A VPN device.
3. What happens to the mgmt→storage test — same mechanism, or a second one? Justify.
4. Write the corrected selector set (all needed pairs). Then: wildcard selectors
   (0.0.0.0/0 ↔ 0.0.0.0/0) — one advantage, one danger.

### Expected learning outcomes
- Separate routing decisions from VPN traffic-selection decisions.
- Diagnose partial-connectivity from selector scope.
- Design explicit selector pairs vs wildcard trade-offs.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The route says *where*; the selector says *whether*. A packet can be pointed at
   a tunnel that refuses to carry it."
2. "Count the pairs the business needs: 3 HQ subnets × 2 co-lo subnets. How many
   selector pairs exist?"

### Solution
1. Gate 1 — routing: "what next hop/interface serves this destination?" (FIB lookup;
   all five remote subnets route via the tunnel ✓). Gate 2 — IPsec policy/selector:
   "does this packet's src/dst pair match an configured selector?" Only then is it
   encrypted and sent; non-matching packets are dropped or sent unencrypted per
   policy (here: dropped, hence timeouts).
2. staff→compute: routes ✓ (10.30.10.0/24 via tunnel), but the selector pair is
   10.20.40.0/24 ↔ 10.30.10.0/24 only — 10.20.30.9 (staff) matches *no* selector ⇒
   the VPN device drops it (or leaks it — here dropped, per the timeout). The tunnel
   never sees the packet; encrypt counters stay flat.
3. Same mechanism, second pair: mgmt→storage fails because *no* selector covers
   10.20.50.0/24 ↔ 10.30.20.0/24 (and also 10.30.20.0/24 appears in no selector at
   all). Two failures, one root cause: selector scope was defined for one pair and
   never extended with the subnets.
4. Corrected selectors (explicit pairs, 3×2 = 6):
   10.20.30.0/24 ↔ 10.30.10.0/24; 10.20.30.0/24 ↔ 10.30.20.0/24;
   10.20.40.0/24 ↔ 10.30.10.0/24; 10.20.40.0/24 ↔ 10.30.20.0/24;
   10.20.50.0/24 ↔ 10.30.10.0/24; 10.20.50.0/24 ↔ 10.30.20.0/24.
   Wildcard (0.0.0.0/0 ↔ 0.0.0.0/0): advantage — new subnets work without selector
   edits (ops win). Danger — the tunnel will also *grab* traffic meant for the
   internet (0.0.0.0/0 matches everything), silently blackholing or misrouting it;
   also blurs the security boundary (everything crosses the tunnel by default).
   Middle path: summary selectors (e.g., 10.20.0.0/16 ↔ 10.30.0.0/16) if addressing
   is plan-consistent.

### Reasoning process
Facts: selectors (one pair), routes (all five), counters (track one pair), three
test outcomes. Model: two-gate model (route ∧ selector). Each failing test = missing
selector pair; fix = enumerate the needed pairs (or justify summaries/wildcards).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Add static routes for the failing subnets" | Routes already exist for all five; the second gate is the blocker |
| "Rekey/restart the tunnel" | Phase 2 is *up* and encrypting its one pair; the fault is scope, not state |
| "Use one big /16 selector on each side" | Works only if the address plan is clean — here it is, but state the assumption; mixing unselected ranges into a /16 can over-grab |
| "NAT everything through the tunnel" | Masks the selector design and breaks end-to-end identity; a workaround pretending to be architecture |

### Extension question
The team adds a *second* VPN (different vendor) carrying the same subnets for
redundancy. What new failure mode appears at the selector level, and what routing
control keeps the two tunnels from fighting over the same prefixes? (Overlapping
selectors across devices ⇒ ambiguous policy match; control: distinct selector sets
per tunnel + route metrics/preference (or policy-based routing) so only one tunnel
owns each prefix at a time ⚠ vendor-dependent failover behavior.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Two-gate model crisp; each failing test attributed; six explicit pairs or justified summary; wildcard trade-off with the over-grab danger |
| 3 Proficient | Correct diagnosis; selector set incomplete or unjustified wildcards |
| 2 Developing | "VPN misconfigured" without the routes-vs-selectors split |
| 1 Beginning | Reboots the VPN |

### References
- PD §8.8 (IPsec: SAs, selectors) ⚠ verify section mapping
- Kurose & Ross §8.8 (IPsec and VPNs); RFC 4301 (SPD/selector semantics)
