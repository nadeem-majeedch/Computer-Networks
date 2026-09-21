# PB-062 — Design Review: The Campus Upgrade (L31, Advanced)

| Field | Value |
|---|---|
| Difficulty | **Advanced** |
| Lecture(s) | L31 — Enterprise Design & the Data-Science Connection |
| CLOs | CLO6 (design methodology + trade-off defense), CLO5 (capacity reasoning) |
| In-class slot | Extended activity; 30 min, groups of 3–4 → review board |
| Case type | Design + trade-off defense · Topic: Enterprise network design |
| Evidence policy | Synthetic requirements + a flawed proposal, labeled; every critique must cite a requirement or a named failure mode |

---

## Student version

### Scenario
Meridian HQ-A grows: the analytics cluster doubles, wireless density triples, and the
building link (1 Gb/s, shared by everything) is the known bottleneck. The junior
architect's proposal landed this morning. You're the review board.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Requirements (from the stakeholder minutes):
  R1  Analytics cluster (HQ-A) ↔ HQ-B daily transfers ≤ 30 min for 500 GB
  R2  Wireless: 3× current AP density on floors 2–4; PoE budget for 40 new APs
  R3  Zero-forced-outage migration (business hours traffic cannot stop)
  R4  Segment: analytics cluster traffic must not share a broadcast domain
      with staff (PB-026's subnets remain)
  R5  Budget: one 10 Gb/s inter-building link OR two 1 Gb/s links (same price)

The proposal:
  P1  Buy the two 1 Gb/s links ("redundancy beats capacity")
  P2  Upgrade the HQ-A core switch to a bigger box, one flat 10.20.0.0/16 for
      everything ("simplifies routing")
  P3  Replace floor switches with PoE models; hang APs off access switches
  P4  Migrate during a Saturday window ("zero forced outage = weekend work")
The review must check each against R1–R5 and the failure modes it invites.
```

### Problem statement
Review P1–P4 against the requirements: pass/fail each with the specific requirement
or failure mode cited, then produce your corrected plan (staged, honoring R3) with
the one big trade-off you'd defend to the CFO.

### Evidence pack
The labeled synthetic requirements and proposal. Numbers to use: 500 GB ≤ 30 min
⇒ ≥ 2.22 Gb/s effective (compute it: 500×10⁹ B×8 ÷ 1800 s ≈ 2.22 Gb/s). The flat
/16, the single-window migration, and the PoE budget each hide a specific
failure mode — find them.

### Constraints
- Pass/fail must cite R-numbers or named failure modes — no adjectives.
- The corrected plan must be *staged* (R3) and must state what remains broken
  until the final stage.

### Student questions
1. R1 arithmetic: what effective throughput does the 30-minute budget demand, and
   what does P1's "two 1 Gb/s links" actually deliver for *one* flow? (Hint: PB-006
   and window math; and ECMP per-flow hashing ⚠.)
2. P2's flat /16: which requirement does it violate, and which *past* case study
   predicts the operational pain? (PB-026/PB-024/PB-017 all apply — name the
   mechanism, not the case number.)
3. P3's PoE plan: what's missing between "PoE switch" and "40 APs at 25 W each"?
   Compute the budget and name the failure.
4. P4 vs R3: is a Saturday window "zero forced outage"? Distinguish planned outage
   from forced outage — and redesign the migration in three stages.
5. The CFO trade-off: one sentence each for two 1 Gb/s vs one 10 Gb/s — then your
   recommendation tied to R1's arithmetic.

### Expected learning outcomes
- Convert business requirements to network arithmetic before choosing gear.
- Map proposals to requirements and failure modes, not preferences.
- Stage migrations that honor availability constraints.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "R1 is an arithmetic requirement, not a vibe. Convert 500 GB / 30 min into a
   rate — then ask what a single TCP flow can extract from two 1 Gb/s links."
2. "P2 deletes the segmentation requirement for convenience. Which past incidents
   predicted the cost of flat networks — name mechanisms: ARP churn, broadcast
   storms, address-plan collapse."

### Solution
1. R1: 500×10⁹×8 ÷ 1800 ≈ **2.22 Gb/s effective**. Two 1 Gb/s links with ECMP
   per-flow hashing: one TCP flow rides *one* link (1 Gb/s ceiling) unless the
   transfer parallelizes itself; a window-bound flow (PB-006) may fall further
   short. So P1 *fails R1* for single-flow behavior and only approaches it with
   multi-connection tooling (which the cluster's sync tool may not do ⚠ — survey
   question). The 10 Gb/s single link passes with headroom.
2. P2 violates **R4** (explicit segmentation) — and the *mechanisms* past cases
   taught: flat /16 → address-plan arithmetic collapses (no VLSM growth lanes,
   PB-026), duplicate-IP blast radius grows (PB-024 — one lab PC now contests the
   whole campus), VLAN-accident scope grows (PB-017 — a mislabeled port exposes
   segments campus-wide), broadcast/storm domain spans buildings (PB-016).
   Fail P2 with mechanisms; a corrected P2 keeps L3 boundaries per subnet group
   and a sane address plan.
3. P3: 40 APs × ~25 W (802.3at-class for good APs ⚠) = **1,000 W** of PoE budget
   on the floors — access switches must be sized for PoE *plus* their existing
   wired load; the proposal names no budget. Failure mode: switch PoE pools
   exhausted mid-deployment → APs boot-loop or APs negotiate down to lower
   classes. Fix: per-floor PoE budget audit + uplink power planning.
4. P4: a Saturday window is a *planned* outage, not "zero forced outage" — R3
   says business-hours traffic cannot stop; a Saturday migration forces weekend
   staff (the DS team's Friday-night jobs!) offline. Violation by redefinition.
   Three-stage migration: (1) run the new 10 G link *parallel* to the old 1 G
   (both live, load-share or shadow); (2) move workload classes one at a time
   (analytics first — R1's pain) with rollback = unplug the new path; (3) retire
   the 1 G link only after a week of clean metrics (PB-057's event-based
   monitoring watches the cutover).
5. CFO: two 1 Gb/s = redundancy *if* they're true diverse paths (ask! same conduit
   = same backhoe) but fails R1 arithmetic; one 10 Gb/s = 4.5× the R1 requirement
   but is a single point of failure — mitigations: service-protection via the
   staged parallel-run period and a documented 1 G fallback (the *old* link kept
   alive as emergency spare during stage 3 — costs nothing, answers the CFO).
   Recommend: **one 10 Gb/s + old 1 Gb/s retained as emergency path**.

### Reasoning process
Facts: five requirements, four proposal lines. Method: requirement → arithmetic →
proposal verdict (cited) → corrected staged plan → executive trade-off. Every
"fail" carries its mechanism from the case bank's own lessons — the review *is* the
synthesis.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Both links, because redundancy" | Uncited preference; R1 arithmetic disagrees — and 'redundant' links in one conduit aren't redundant (ask the conduit question) |
| "Flat network, QoS will sort it" | QoS cannot create segmentation (R4) or fix address-plan collapse |
| "Migrate Saturday = satisfies R3" | Redefines the requirement; R3 protects *business-hours* traffic — weekend jobs count |
| PoE "should be fine" | 1,000 W is a planning number, not a vibe; unbudgeted PoE is a deployment-time surprise |

### Extension question
The CFO asks: "what breaks first if we approve your plan and do *nothing else* for
two years?" Build the two-year risk list from the plan's residual gaps (single 10 G
link failure mode; Wi-Fi 6E/7 PoE class growth; the analytics cluster's own
east-west bandwidth — inter-building was fixed, intra-building wasn't measured ⚠ —
say what you'd monitor to see it coming).

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | R1 arithmetic drives P1 verdict; P2/P3/P4 fails carry mechanisms; staged plan with rollback; CFO trade-off tied to numbers |
| 3 Proficient | Correct verdicts; staging or trade-off thin |
| 2 Developing | Reviews by preference, uncited |
| 1 Beginning | Approves the proposal |

### References
- Course case bank PB-006, PB-016, PB-017, PB-024, PB-026 (mechanisms cited above)
- PD §6.4/§8 design context ⚠ verify section mapping
