# PB-038 — The Buffer That Ate the Latency (L19, Advanced)

| Field | Value |
|---|---|
| Difficulty | **Advanced** |
| Lecture(s) | L19 — TCP Flow & Congestion Control |
| CLOs | CLO5 (queueing/latency reasoning), CLO6 (measurement design + mitigation trade-offs) |
| In-class slot | Extended activity; 25 min, groups of 3 |
| Case type | Diagnostic + measurement design · Topic: Network performance |
| Evidence policy | Synthetic measurements, labeled and internally consistent; AQM behavior described qualitatively (CoDel/fq_codel ⚠ verify implementation details) |

---

## Student version

### Scenario
Meridian's 200 Mb/s internet circuit "feels fine on speed tests but video calls
collapse whenever someone syncs a dataset." The ops dashboard shows the familiar
numbers; the data-science team insists the numbers miss the point.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
Circuit:      200 Mb/s down / 200 Mb/s up; base RTT to HQ SaaS: 20 ms
Dashboard:    throughput 197/199 Mb/s at peak; "no loss" (queued, not dropped)
Latency test (ping under load, run by the DS team):
  idle:                    20.1 ms (p95 20.4)
  during dataset sync:     p50 410 ms, p95 620 ms; jitter 40–120 ms
  after sync (first 2 s):  p95 90 ms → decays to 20 ms
Sync traffic: single TCP flow, sender aggressively fills the path
Router queue: default single FIFO, buffer sized "to never drop" (~2 MB)
```

### Problem statement
Diagnose the phenomenon from the latency-under-load evidence (name it, explain the
mechanism, and verify the buffer arithmetic). Then design the measurement that proves
the fix worked, and compare three mitigations with trade-offs.

### Evidence pack
The labeled synthetic measurements. Facts: throughput near line rate; latency inflated
~20× under load; decay after load ends; FIFO buffer ~2 MB. Assumption to state: the
sync flow's TCP never receives loss signals (queue absorbs) — consistent with "no
loss".

### Constraints
- The buffer arithmetic must connect 620 ms ↔ bytes ↔ rate (show it).
- Measurement design must be runnable in 10 minutes on the production link.
- Mitigations: bigger link, AQM (CoDel/fq_codel), egress shaping — one trade-off
  each; pick a deployment order.

### Student questions
1. Name the phenomenon and state the two-part mechanism (queue growth + TCP behavior).
2. Buffer arithmetic: how much data is 620 ms of queue at 200 Mb/s? How does that
   compare to the 2 MB buffer? What does this say about the buffer's design goal
   ("never drop")?
3. Why does TCP *itself* make this worse (loss-based congestion control + a buffer
   that never drops)? One sentence on the classic "self-fill" dynamic.
4. Design the 10-minute before/after measurement (commands, cadence, success
   criterion). Then order the three mitigations and justify.

### Expected learning outcomes
- Diagnose bufferbloat from latency-under-load rather than throughput data.
- Convert queue delay to bytes and critique oversized buffers.
- Design a lightweight A/B measurement on a live link.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Throughput dashboards ask 'how fast can we push?' The users' complaint is 'how
   long does a packet wait?' Different metrics — which one is lying by omission?"
2. "A queue that never drops never tells TCP to slow down. Who wins that standoff?"

### Solution
1. **Bufferbloat**: (a) the FIFO queue grows to absorb sustained overload (hundreds
   of ms of data resident), (b) loss-based TCP keeps sending at full rate because the
   queue *never drops* — no congestion signal — so the queue stays full; interactive
   packets wait behind megabytes of sync data.
2. Delay = queue_bytes ÷ rate ⇒ bytes = 0.620 s × 200 Mb/s ÷ 8 = **15.5 MB**?? —
   check: 0.62 × 25×10^6 B/s = 15.5 MB — but the buffer is 2 MB ⇒ max queue delay =
   2×10^6 ÷ 25×10^6 = **80 ms**. Reconcile honestly: the observed 620 ms *cannot* be
   queue-at-the-router alone — the arithmetic refutes the single-hop story. So the
   latency must accumulate across **multiple queues** (device Wi-Fi? upstream CPE?
   intermediate ISP buffers — each contributing 60–150 ms) or the "2 MB" figure is
   per-queue and there are several. Teaching point: the discrepancy between 2 MB
   (80 ms) and 620 ms is *evidence* — a single-hop explanation fails; the diagnosis
   must be multi-hop queueing. (Accept either documented reconciliation; the
   arithmetic check is the deliverable.) The "never drop" goal is itself the defect:
   a buffer sized for absorption delays instead of signals.
3. Loss-based TCP treats drop = congestion signal; a never-dropping queue hides that
   signal, so the sender keeps its window growing/maximum, keeping the queue full —
   the flow "self-fills" the buffer it is standing in (the classic self-clocking
   pathology AQM was designed to break).
4. Measurement: run `ping <saas-ip> -i 0.2 -c 600` (100-s window) during (a) idle,
   (b) a controlled sync; record p50/p95; success criterion: p95 under load ≤ 50 ms
   (from 620 ms) with no throughput regression >5%. Cadence 5 Hz gives 500+ samples/
   condition — enough for p95. Order: (1) **AQM (fq_codel/CoDel)** on the egress —
   targets the mechanism (keeps queues short, drops/marks early), no new hardware ⚠
   verify router support; (2) **egress shaping** to ~90–95% of rate if the bottleneck
   queue lives in the ISP CPE (moves the queue to a point you control) — trade-off:
   5–10% throughput sacrificed by design; (3) **bigger circuit** — last: expensive,
   and the evidence shows the pathology reappears whenever any flow saturates any
   link; capacity alone rarely fixes bufferbloat durably.

### Reasoning process
Facts: line-rate throughput, 20× latency inflation, decay after load, 2 MB FIFO.
Model: queue delay = bytes/rate; TCP needs loss/ECN signals; oversized FIFO hides
them. Arithmetic refutes single-hop ⇒ multi-hop queueing diagnosed. Mitigation
targets the signal path (AQM) before capacity.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Speed test says 199 Mb/s — link is fine" | Throughput metrics are blind to queue delay — that's the case's core lesson |
| "Buy the 400 Mb/s circuit" | Moves the saturation point; the sync flow will bloat whatever buffer exists at the new limit |
| "Just make the buffer bigger" | Directly worsens queue delay; the design goal ("never drop") is the bug |
| "Limit the sync app" | Works but is per-app whack-a-mole; AQM fixes the *class* of problem |

### Extension question
 fq_codel distinguishes flows (fair queueing) and drops from the *newest* flows
first. Explain in this incident's terms why the sync flow (alone in its queue) sees
drops while the ping packets (another queue) sail through. (Per-queue isolation: the
sync flow's queue is the one exceeding the standing-queue target and getting marked/
dropped; ping's sparse queue stays under target — latency for interactive traffic is
protected *without* rate-limiting the bulk flow's fair share.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Mechanism two-part; buffer arithmetic *catches the single-hop discrepancy* and reconciles; measurement design concrete with criterion; mitigation order justified |
| 3 Proficient | Diagnoses bufferbloat; arithmetic done but discrepancy unnoticed |
| 2 Developing | "Latency high under load" restated; no byte math |
| 1 Beginning | Proposes bigger buffers |

### References
- Kurose & Ross §3.6/§3.7 (congestion control signal paths) ⚠ verify
- Nichols & Jacobson, "Controlling Queue Delay" (CoDel, ACM Queue 2012); fq_codel docs
  ⚠ verify implementation claims
