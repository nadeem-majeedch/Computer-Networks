# Lecture 04 — Performance, Measurement & Quality of Service — Slide Deck

| Field | Value |
|---|---|
| Slides | 17 (120 min: 10 open · 40 teach · 5 break · 55 LAB-01 · 10 wrap) |
| Companions | [`notes.md`](notes.md) · [`worksheet.md`](worksheet.md) · [LAB-01](../../labs/lab-01-latency-throughput/README.md) |
| Style | [Course deck conventions](../../lectures/README.md#deck-conventions) |

## Deck outline

| # | Slide | # | Slide |
|---|---|---|---|
| 1 | Title | 10 | LAB-01 brief |
| 2 | Hook: the lying speed test | 11 | Lab walkthrough cues |
| 3 | Measurement vocabulary | 12 | Classroom questions |
| 4 | RTT: what ping really says | 13 | Worked example: baseline judgment |
| 5 | Throughput: iperf3's contract | 14 | Common pitfalls (measurement) |
| 6 | Jitter & loss in numbers | 15 | Summary |
| 7 | Baselines: the concept | 16 | Exit question |
| 8 | Estimation vs measurement | 17 | Lab safety/setup slide |
| 9 | Worked example: predict then measure | | |

## Slides

### Slide 1 — Title
**Computer Networks — Lecture 4**
Performance lab foundations: measuring the network

> Notes — First real lab. The skill: numbers you can defend, not numbers you hope for.

### Slide 2 — Hook: the lying speed test
- Two speed tests, same desk: 92 vs 61 Mb/s
- Same network. Which is wrong?
- Both — and that's today's lesson

> Notes — 3 min pair-discuss. Land on: every measurement has context (server, time, method); "wrong" is usually "different question."

### Slide 3 — Measurement vocabulary

| Term | Question it answers | Tool |
|---|---|---|
| Latency/RTT | how long per round trip? | ping |
| Throughput | how many bits/s sustained? | iperf3 |
| Jitter | how much does RTT vary? | ping stats |
| Loss | what fraction disappears? | ping -c / iperf3 |

> Notes — This table is the lab's backbone; keep it visible during LAB-01. Each tool's *method* matters more than its number.

### Slide 4 — RTT: what ping really says
- min / avg / max / mdev — read all four
- min ≈ best-case path cost; max−min ≈ queueing's fingerprint
- ICMP replies can be rate-limited (asymmetric treatment)

> Notes — Demo cue: ping a busy host vs the lab gateway; compare mdev. ICMP rate-limiting previews L16.

### Slide 5 — Throughput: iperf3's contract
- Measures TCP/UDP throughput *between two endpoints you run*
- Reports what the flow achieved — never the link's "speed"
- Parallel streams (`-P`) test different limits

> Notes — The contract: reproducible commands or the number doesn't exist (course evidence rule, first sighting).

### Slide 6 — Jitter & loss in numbers
- Jitter ≈ spread of RTT samples (mdev is a proxy)
- Loss: retransmits hide it from TCP users — until latency spikes
- Video apps feel loss/jitter before file transfers do

> Notes — Connect to L01's taxonomy; now it's numbers. iperf3 UDP mode makes loss *visible* (`-u -b`).

### Slide 7 — Baselines: the concept
- A measurement is meaningful **vs a baseline**
- Baseline = same method, same context, quiet period
- Change vs noise requires distributions, not single points

> Notes — The course's most transferable networking habit. Preview L29: dashboards are baselines with memory.

### Slide 8 — Estimation vs measurement
- **Estimate**: physics + arithmetic (L01 delay math, BDP)
- **Measure**: run and observe (today)
- Estimate first — it predicts what measurement *should* say

> Notes — The worksheet's estimate column forces the habit: prediction → measurement → explanation of the gap.

### Slide 9 — Worked example: predict then measure
- Predict: 100 Mb/s link, 20 ms RTT, single stream — what iperf3 max?
- Window-limited: if rwnd ≈ 64 kB → ≈ 64 kB/20 ms ≈ **25.6 Mb/s**
- Measure: record actual; explain the gap

> Notes — The "gap explanation" is the graded skill. Notes.md §4 has the full worked variant with a 512 kB window.

### Slide 10 — LAB-01 brief
- Pairs · measure latency, throughput, jitter, loss
- Estimate column first, then measure, then explain
- Submit: commands + numbers + gap explanations

> Notes — 55 min. Rubric: results 40 / analysis 30 / reproducibility 20 / clarity 10 (practical-work-rubric). Announce the drop-lowest rule once, semester-wide.

### Slide 11 — Lab walkthrough cues
- Station setup: two namespaces or two VMs per pair
- `ping -c 20`, then `iperf3 -s` / `iperf3 -c`
- Save outputs as you go; no reconstructed numbers

> Notes — Circulate for the classic errors: iperf3 server missing, units confusion (Mb/s vs MB/s).

### Slide 12 — Classroom questions
1. Your ping min is 21 ms, max 25 ms. What lives in the 4 ms?
2. iperf3 shows 94 Mb/s on "100 Mb/s". Give two defensible causes.
3. Why run 20 pings instead of 1?

> Notes — Q2 recycles the hook — by now students should split overhead vs window-limit causes with *evidence types* named.

### Slide 13 — Worked example: baseline judgment
- Before change: avg 21.0 ms; after: 23.0 ms; spread was ±5 ms
- Is 2 ms meaningful?
- No — inside baseline noise; collect more samples first

> Notes — The judgment template (compare to spread) transfers to L29 alerting verbatim.

### Slide 14 — Common pitfalls (measurement)
- Measuring the wrong pair (switch in path vs direct)
- Averaging away the tail (max/mdev matter)
- Reporting numbers without commands

> Notes — Pitfalls map 1:1 to rubric deductions; show the mapping so it's fair.

### Slide 15 — Summary
- Four measurements: RTT, throughput, jitter, loss
- Every number needs a baseline and a method
- Estimate → measure → explain the gap
- Next: the physical layer under those numbers (L05)

> Notes — Read the rubric dimensions aloud once; students hear how the lab is graded.

### Slide 16 — Exit question
Which number — min, avg, or max RTT — best reveals congestion, and why?
*(L05: where those milliseconds physically come from.)*

> Notes — Answer: max (or max−min spread) — queueing's fingerprint. Exit slips feed W02 quiz pool.

### Slide 17 — Lab safety/setup slide
- Isolated lab environment only (course safety rules, week-1 acknowledgment)
- No measurements against external hosts without instructor approval
- Teardown: `ip netns del` names; leave stations clean

> Notes — Read the ethics gate line verbatim from the lab syllabus. 60 seconds, non-negotiable.

### Demonstration instructions (instructor)
- Pre-stage: `iperf3 -s` on one namespace per pair; verify loopback-netem variant if wiring is short
- ITI: run LAB-01 once this week; note real min/avg/max values for the plenary compare
- Fallback: worksheet's pre-recorded outputs allow the analysis half offline (labeled synthetic)

### References for the deck
- PD "computer network metrics" sections (throughput/RTT treatment)
- iperf3 manual — measurement semantics and units
- LAB-01 package: [`../../labs/lab-01-latency-throughput/README.md`](../../labs/lab-01-latency-throughput/README.md)
