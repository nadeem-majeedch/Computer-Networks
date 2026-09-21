# PB-034 — Telemetry Can Lose; Commands Can't (L17, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L17 — UDP & the Transport Layer's Job |
| CLOs | CLO5 (loss arithmetic), CLO6 (protocol-selection trade-offs) |
| In-class slot | Main activity; 20 min, pairs → plenary |
| Case type | Design/calculation · Topic: TCP/UDP behavior |
| Evidence policy | Synthetic measurements, labeled; arithmetic desk-checked; loss semantics stated explicitly |

---

## Student version

### Scenario
The sensor gateway speaks two channel types to HQ over the campus Wi-Fi (lossy): a
10 Hz telemetry stream and a low-rate command channel. The intern proposes "make
everything TCP — reliable is better." The firmware team proposes "make everything UDP
— sensors are lossy anyway."

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Link measured: 2.1% datagram loss (bursty, 50–200 ms episodes), RTT 18 ms
Telemetry:     10 samples/s, 64 B payload, per-sample freshness value decays to
               zero after 1 s (a late sample is worthless)
Commands:      ≤1 per 10 s, ~100 B, each MUST eventually execute exactly once
Budget:        gateway CPU is small (retransmit timers acceptable, TCP stack is not
               — firmware constraint, given)
Current:       both channels UDP; command loss observed ~2%/cmd
```

### Problem statement
Evaluate both "make everything X" proposals with numbers. For each channel, choose UDP,
TCP, or UDP+application-reliability (ACK/retry in the app), and justify with the loss
arithmetic and constraints.

### Evidence pack
The labeled synthetic measurements. Facts to respect: freshness decay (late telemetry
is worthless), exactly-once command requirement, no TCP stack on firmware.

### Constraints
- Quantify: expected loss impact per channel (samples lost/s; command failure
  probability/day).
- Firmware constraint is hard: no TCP stack; "add TCP" must be argued against it.
- Application-layer reliability design must state its retry timer logic.

### Student questions
1. Telemetry over UDP as-is: at 10 samples/s and 2.1% loss, how many samples/day are
   lost, and does the freshness rule make that acceptable? Justify.
2. Telemetry over TCP (hypothetically): what does the 2.1% *bursty* loss do to a TCP
   stream's latency during a 200 ms burst? Why might this be *worse* than losing
   samples?
3. Commands over plain UDP: compute the daily probability that at least one command
   fails forever (assume 8,640 commands/day, independent 2.1% loss, no retry).
4. Design the command channel over UDP with app-layer ACK/retry: state the retransmit
   policy and estimate the residual failure probability (show the per-attempt math).

### Expected learning outcomes
- Match reliability mechanisms to *data semantics* (fresh vs must-deliver).
- Quantify loss impact rather than adjective-reasoning ("lossy", "reliable").
- Design minimal application-layer reliability within constraints.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "A lost sample isn't a failure if a fresher one arrives in time. What's the actual
   cost of 2.1% here?"
2. "TCP never gives up — it *waits*. What does a 200 ms gap do to every sample queued
   behind the retransmission?"

### Solution
1. Losses: 86,400 samples/day × 0.021 ≈ **1,814 samples/day** lost — but each lost
   sample is superseded 100 ms later by the next. Freshness rule: a lost sample
   matters only if *consecutive* losses exceed 1 s (10 samples) — probability of 10+
   consecutive losses at p=0.021 independent ≈ 0.021^10 ≈ 1.7×10⁻¹⁷ ≈ never (real
   bursts correlate, but 200 ms bursts = 2 samples — still below the 1 s horizon).
   Verdict: UDP as-is is **acceptable** — losing stale data is the design.
2. TCP during a burst: segments lost → retransmission waits RTO (≥200 ms+); samples
   queued behind the head-of-line block arrive up to seconds late — *every* one of
   them stale by the freshness rule, yet they're delivered (stale data displacing
   fresh). Bursty 2.1% makes head-of-line blocking a periodic freshness-killer. TCP
   here converts "some lost, all fresh" into "none lost, many useless" — worse for
   this semantic.
3. Plain UDP commands: per-command success = 0.979; daily all-success = 0.979^8640 ≈
   e^(8640×ln0.979) ≈ e^(8640×(−0.02122)) ≈ e^(−183.4) ≈ **~0** ⇒ expected
   command-loss count ≈ 8640×0.021 ≈ **181 failed commands/day**. Unacceptable.
4. App-layer ACK/retry over UDP: retry every 2 s (≈10× RTT), up to 5 attempts, dedup
   by command ID (exactly-once at app level). Per-command failure = 0.021^5 ≈
   **4.1×10⁻⁹** ⇒ per day ≈ 8640×4.1e−9 ≈ **3.5×10⁻⁵ commands/day** (~1 failure per
   77 years) — meets the requirement. Timer logic: exponential backoff optional;
   dedup mandatory (retries can duplicate execution).

### Reasoning process
Facts: loss rate/bursts, freshness decay, exactly-once semantics, no-TCP constraint.
Model: reliability value = f(data semantics); quantify each channel's cost under each
transport. Design: UDP + scoped app reliability (ACK+dedup) for commands only.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Reliable = TCP = better" (intern) | Head-of-line blocking destroys freshness semantics; firmware can't run TCP anyway |
| "Sensors are lossy, keep UDP for commands" (firmware team) | 181 failed commands/day — semantics demand reliability *somewhere* |
| "Add retries without dedup" | Retry + no dedup = double-executed commands (exactly-once violated) |
| "Retransmit every lost sample in the app" | Wastes the freshness budget; retransmitting stale data is worse than skipping |

### Extension question
The firmware team later ships a device that *can* run TCP. Does the telemetry answer
change? Argue both sides. (No: semantics unchanged — TCP still head-of-line-blocks
freshness; the budget constraint was one argument among two, and the semantic argument
stands alone. Yes-side: if bursts exceed the 1 s horizon (>1 s loss episodes), TCP's
recovery might beat sample loss — re-measure and re-derive; the method, not the
answer, is the deliverable.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Both quantifications correct; head-of-line mechanism; retry design with dedup and residual-probability math |
| 3 Proficient | Channel choices right; arithmetic partial |
| 2 Developing | Picks transports by category, not semantics |
| 1 Beginning | "TCP everywhere" |

### References
- PD §3.3 (UDP), §3.5 (principles of reliable transfer) ⚠ verify sections
- Kurose & Ross §3.3–3.4 (UDP; principles of reliable data transfer)
