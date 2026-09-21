# PB-008 — Buy Bandwidth or Schedule It? (L04, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L04 — Performance, Measurement & Quality of Service |
| CLOs | CLO5 (delay/queueing reasoning), CLO6 (evaluate trade-offs) |
| In-class slot | Main activity; 20 min, groups of 3 → plenary debate |
| Case type | Trade-off + design · Topic: Network performance |
| Evidence policy | Synthetic measurements, labeled; queueing statements kept qualitative-plus-arithmetic, internally consistent |

---

## Student version

### Scenario
Every evening 22:00–05:30, the nightly backup (see PB-006) saturates the inter-building
link. During that window, interactive traffic — SSH sessions, Git pushes, a browser-based
BI dashboard used by the on-call team — degrades badly. The network manager has budget
for exactly **one** intervention this quarter.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Off-hours (no backup): interactive RTT 2 ms, jitter <1 ms
Backup window:         link utilization ~95%; interactive RTT 45–60 ms,
                       jitter 5–15 ms; occasional dashboard timeouts
Backup goodput:        26.2 Mb/s (window-bound — see PB-006 finding)
Interactive volume:    ~30 Mb/s peak, bursty
Proposal A:            10 Gb/s link upgrade (capex, 6-week lead time)
Proposal B:            QoS: priority queue for interactive + rate-limit/shaping
                       the backup class to ~60% of link (config, zero capex)
Proposal C:            move the backup to 05:30–07:30 (after interactive peak)
```

### Problem statement
Recommend one intervention. Justify with the delay model: explain *why* the backup makes
interactive traffic suffer (queueing), predict the effect of each proposal, and be
explicit about what your recommendation does **not** fix.

### Evidence pack
The labeled synthetic measurements. You may use PB-006's finding (backup is
window-bound, not link-bound) as given. Assumptions to state: bursty arrival behavior;
interactive flows are latency- and jitter-sensitive, not throughput-hungry.

### Constraints
- Exactly one recommendation; secondary options may be mentioned as complements, not
  substitutes.
- Reasoning must reference queueing/utilization, not adjectives like "slow".

### Student questions
1. Why does interactive latency rise from 2 ms to ~50 ms while its own volume barely
   changes? (Name the delay component and the mechanism.)
2. Under Proposal A, what happens to interactive RTT *before* the 6-week lead time
   elapses, and after?
3. Under Proposal B, predict RTT and backup goodput. What risk does shaping introduce?
4. Which proposal do you recommend, and what does it not fix?

### Expected learning outcomes
- Attribute latency inflation to queueing at high utilization, not to "less bandwidth
  for me".
- Predict mitigation effects from the delay model rather than intuition.
- Recognize that scheduling (when) can substitute for capacity (how much).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Interactive packets share one queue with 26 Mb/s of backup. What happens to their
   wait time when the queue is nearly full?"
2. "The backup is window-bound at 2.6% of link capacity — yet utilization hits 95%.
   What must the *other* traffic be doing during that window? Check the evidence
   carefully." (Expected: interactive + the on-call BI dashboard + replication traffic
   listed in constraints is NOT in evidence — the correct response is to notice the
   inconsistency: 26.2 Mb/s + 30 Mb/s ≠ 95% of 1 Gb/s. Strong students *flag the
   evidence gap* — reward this; plausible fillers: other scheduled jobs, monitoring
   streams — labeled assumptions.)

### Solution
1. Queueing delay. At ~95% utilization, queues are almost always non-empty; an
   interactive packet waits behind a burst of backup packets. The 2→50 ms rise is
   (almost) entirely wait-in-queue — propagation is unchanged.
2. Before A lands: unchanged ~50 ms for six more weeks. After: queueing delay collapses
   (same arrival rate, 10× service rate → utilization ~9.5% → RTT returns to ≈2–3 ms).
   Correct but slow and expensive.
3. B: interactive packets get priority → their queueing delay drops to ≈0 (they jump
   the backup queue); interactive RTT ≈ 2–3 ms. Backup goodput falls to ≈60% of link
   (~600 Mb/s shared) — but it's window-bound at 26.2 Mb/s anyway, so shaping the
   backup *costs it nothing* unless the window fix (PB-006 C) lands first; risk: a
   mis-sized shaper can starve legitimate bulk traffic or leave the priority queue
   unpoliced (interactive burst must still be capped or it can starve backup entirely).
4. Recommend **B** (plus PB-006's buffer fix as the true root-cause remedy): zero capex,
   immediate, and targeted at the actual mechanism (queueing). Does not fix: absolute
   capacity growth if the org later needs >1 Gb/s of *real* aggregate throughput; also
   does nothing for the backup's own 8.5-hour runtime (that's PB-006's window fix).

### Reasoning process
Facts: utilization 95% in-window, interactive delay ↑ 25×, backup window-bound.
Model: latency inflation = queueing; mitigations act on (a) service rate (A), (b)
scheduling (B), (c) arrival timing (C). Predict each; pick the cheapest mechanism that
targets the binding constraint now, note the true root cause (PB-006) as the durable fix.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| A because "bandwidth fixes everything" | Fixes it 6 weeks late at high capex; B fixes it in a day |
| B with backup left at 100% priority | Defeats the purpose: the bulk class would still monopolize |
| Choosing C alone | Shifts congestion to 05:30–07:30 — the BI morning peak now collides with it; better as a complement |
| Jitter "must be a wireless problem" | No wireless on the path; don't invent media |

### Extension question
Suppose the on-call dashboard traffic were equally *volume*-heavy (300 Mb/s sustained,
also latency-sensitive). Re-evaluate A vs B. (B's priority queue now carries 30% of load
— still viable but headroom shrinks; if interactive aggregate approaches link capacity,
no scheduler can create bandwidth that isn't there: capacity, then scheduling.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Queueing mechanism explicit; per-proposal predictions quantified; flags the 95%-vs-26 Mb/s evidence gap; recommendation scoped (what it doesn't fix) |
| 3 Proficient | Mechanism + predictions correct; misses evidence gap |
| 2 Developing | Picks B by intuition; predictions hand-wavy |
| 1 Beginning | "More bandwidth" without model |

### References
- PD §1.4.2 (queuing delay and utilization), §4.2 (scheduling mechanisms)
- Kurose & Ross §1.4.2; §4.4 (scheduling and policing, QoS framing)
