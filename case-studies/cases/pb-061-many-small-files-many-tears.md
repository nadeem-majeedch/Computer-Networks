# PB-061 — Many Small Files, Many Tears (L31, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L31 — Enterprise Design & the Data-Science Connection |
| CLOs | CLO5 (overhead vs bandwidth regimes), CLO6 (mitigation ranking) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Calculation + diagnosis · Topic: Data-science networking |
| Evidence policy | Synthetic measurements, labeled; arithmetic desk-checked; TCP startup behavior as teaching model |

---

## Student version

### Scenario
The ML pipeline ingests **10,000 small files (50 KB each)** from HQ-B to the HQ-A
cluster every morning over the inter-building link (1 Gb/s, RTT 20 ms, otherwise
idle). The run takes **41 minutes**. A teammate's "obvious" fix: buy the 10 Gb/s
upgrade from PB-062. Before anyone signs anything, do the arithmetic.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Link:     1 Gb/s, RTT 20 ms, idle during the ingest window
Workload: 10,000 files × 50 KB (51,200 B on disk)
Tool:     sequential per-file transfers, one TCP connection per file,
          connection re-established for each file (no keep-alive, no pipelining)
Measured: 41 min wall clock; per-file transfer ≈ 246 ms average
Analysis inputs:
  ideal transfer time for 500 MB total at 1 Gb/s: 500×10⁶×8 ÷ 10⁹ = 4.0 s
  TCP slow start: a 50 KB file needs ~3 RTTs of window growth to deliver
      (exponential cwnd: 10→20→40 MSS-class segments; 50 KB ≈ 35 segments ⚠
      simplified model — IW=10)
  per-file connection setup: TCP handshake = 1 RTT before any data
```

### Problem statement
Build the per-file time budget (handshake + slow-start-limited transfer + teardown),
compute the theoretical serial time, reconcile with the measured 246 ms/file, name
the regime (bandwidth-bound vs overhead-bound), and rank three fixes by
expected impact.

### Evidence pack
The labeled synthetic measurements. Facts: sequential per-file connections, 50 KB
files, 20 ms RTT, 41 min total. The simplified slow-start model is given — use it,
state it.

### Constraints
- Reconciliation must be arithmetic: 246 ms/file must decompose into named
  components (show your per-component assumptions).
- Ranking must quantify each fix's effect (no "it would help").

### Student questions
1. Per-file *floor*: handshake RTT + minimal data phase at slow start (use the
   given model: 50 KB ≈ 35 segments, cwnd 10→20→40 → ~2 RTTs of data after the
   handshake RTT). What's the minimum wall time per file?
2. ×10,000 files: theoretical serial time. How does it compare to the measured
   41 min? What does the residual represent (label your assumptions)?
3. Name the regime. Would the 10 Gb/s upgrade fix it? Show the new floor.
4. Rank: (a) 10 Gb/s upgrade, (b) parallel transfers (e.g., 16 concurrent
   connections), (c) batch/pack the files (tar-like single stream). Quantify
   each's effect on the 41 minutes.

### Expected learning outcomes
- Decompose transfer time into protocol overhead vs data time.
- Recognize overhead-bound regimes where bandwidth upgrades don't help.
- Rank mitigations by quantified impact.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "One file = 1 RTT of handshake + ~2 RTTs of slow-start data + wire time. At
   20 ms RTT, how many ms is that — and what fraction of it is *data*?"
2. "The upgrade multiplies the smallest term. The protocol overhead term is
   untouched. Which term dominates?"

### Solution
1. Per-file floor (teaching model): handshake = 1 RTT = 20 ms; data: 35 segments
   over cwnd growth 10/20/40 ⇒ ~2 RTTs = 40 ms; wire time for 51,200 B at 1 Gb/s
   ≈ 0.41 ms (negligible); teardown ≈ 0.5 RTT ≈ 10 ms. Floor ≈ **70 ms/file**
   (state: model ignores ACK granularity and receiver-window limits — assumptions).
2. ×10,000 = **700 s ≈ 11.7 min** theoretical. Measured 41 min ⇒ residual ≈
   29 min ⇒ +175 ms/file unexplained by the floor: real-world components —
   per-file connection *setup* at the application layer (TLS? auth? directory
   metadata), filesystem overhead (10,000 creates/closes), server-side per-request
   processing. Each is an *assumption* (label them); the honest decomposition:
   floor 70 ms + app/OS overhead ~175 ms — all independent of link speed.
3. **Overhead-bound**: data time is 0.41 ms of ~246 ms per file — 0.17%. A 10 Gb/s
   upgrade shrinks the 0.41 ms to 0.04 ms — wall clock stays ≈41 min (the upgrade
   fixes a term that isn't the problem). New floor at 10G: ~69.6 ms/file —
   indistinguishable.
4. (a) 10 Gb/s: ≈0 min saved (≈41 min — proven above). (b) 16 parallel
   connections: divides the *serial* component by ~16 ⇒ ≈41/16 ≈ **2.6 min** —
   bounded by per-connection overhead but massive win; cost: 16× connection load
   on servers (and fairness on shared links — fine here, idle). (c) Batch to one
   stream: 500 MB as one TCP flow, slow start ramps (⩾35 segments in ~2 RTTs,
   then window-limited): time ≈ RTT-limited ramp + 4 s wire time ≈ **seconds
   (~10–20 s total)** — the best fix; cost: changes the pipeline (compression?
   integrity per file?), operational work vs (b)'s config change. Ranking: (c) >
   (b) ≫ (a); note (b) is the pragmatic first step, (c) the durable one.

### Reasoning process
Facts: file count/size, RTT, measured wall clock, per-connection pattern. Model:
per-file time = protocol floor (RTT-driven) + app/OS overhead ≫ wire time ⇒
overhead-bound. Mitigations evaluated against the *dominant* term: parallelize or
eliminate the per-file handshake — not more bandwidth.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Buy 10 Gb/s" (PB-062's link is for *other* reasons) | Shrinks the 0.17% term; wall clock unchanged — the arithmetic is the refutation |
| "Enable jumbo frames" | 50 KB files already ship in ~35 packets; frame size is nowhere near the bottleneck |
| "Compress the files" | Same packet count after compression if already-compressed; latency terms untouched |
| "More parallel connections, 512 of them" | Wins first, then collapses under server accept-queue/port exhaustion; parallelism has a knee — 16–64 is the sane band (state it) |

### Extension question
The team adopts (c) but must still support per-file *resumability* after failures.
Design tension: one stream vs per-file restart semantics. Sketch the compromise
(batched chunks + a manifest with per-file offsets + range-retry) and name the
network-level property that makes it work. (Chunked single stream with a manifest:
retransmit only failed byte ranges (TCP already does this *within* a stream) and
re-request failed chunks by offset — works because TCP provides reliable ordered
byte delivery per stream; the manifest moves the *file* semantics to the
application layer, where resumability belongs.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Per-file decomposition with labeled assumptions; regime named with the 0.17% contrast; quantified ranking; knee-of-parallelism honesty |
| 3 Proficient | Floor arithmetic right; ranking partially quantified |
| 2 Developing | "Latency-bound" without decomposition |
| 1 Beginning | Endorses the upgrade |

### References
- Course case PB-006 (window-bound contrast) and PB-006 extension (BDP arithmetic)
- Kurose & Ross §3.5.2 (RTT-limited transfers), §3.7 (slow start) — teaching model
  ⚠ simplified; real IW/initial window per RFC 6928 ⚠
