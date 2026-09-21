# PB-040 — Design Review: "I Invented Reliable UDP" (L20, Advanced)

| Field | Value |
|---|---|
| Difficulty | **Advanced** |
| Lecture(s) | L20 — Programming the Transport Layer: Reliability over UDP |
| CLOs | CLO4 (protocol design evaluation), CLO6 (predict behavior from design) |
| In-class slot | Extended activity; 25 min, groups of 3 → review board format |
| Case type | Design critique · Topic: Network programming |
| Evidence policy | Synthetic spec, labeled; every predicted failure follows from standard transport principles; no fabricated benchmarks |

---

## Student version

### Scenario
A promising student designed "FastSync", a reliable UDP protocol for the cluster.
Before any code ships, the class runs a design review. The spec (verbatim, from the
student's README):

**Synthetic evidence — prepared for this case; a design document, not test results:**

```
FastSync v0.1 spec:
  F1  Fixed retransmit timer: 200 ms for every packet, every network
  F2  Fixed sending window: 64 packets, regardless of network conditions
  F3  No congestion response: "we tested on our LAN, loss is the cable's fault"
  F4  Receiver ACKs every packet individually; sender resends any packet not
      ACKed within 200 ms — including packets the receiver re-ACKs after dupes
  F5  No handshake or connection ID; receiver accepts packets from any source
      matching the UDP port
  F6  Data integrity: "UDP already has a checksum"
Deployment target: cluster sync over the shared 200 Mb/s office uplink
                   (RTT 5–40 ms depending on building) + occasional branch links
                   (RTT 150 ms)
```

### Problem statement
You are the review board. For each spec line, predict the failure mode (with the
network conditions that trigger it), rate severity, and propose the minimal patch.
Then give the overall verdict: ship, fix-then-ship, or redesign — and why.

### Evidence pack
Synthetic evidence — prepared for this case; a design document and deployment
targets, not test results; not from a live system. Each prediction must be *derived* (from
transport principles), not asserted. Where two readings of a line are possible, state
both and what would distinguish them.

### Constraints
- Every flaw needs: mechanism → trigger condition → consequence → minimal patch.
- Severity ratings must be argued (what breaks, for whom, how visibly).
- Patches must stay within "reliable UDP" (no "just use TCP" as the whole answer —
  but you may *recommend* it as a verdict with justification).

### Student questions
1. F1: what breaks on the 150 ms branch link, and on the 5 ms LAN link? Give both.
2. F2+F3 together: what happens to the shared office uplink when two FastSync hosts
   and an SSH session share it? (Predict the latency and fairness outcome.)
3. F4: quantify the ACK overhead at full window (ACKs per data packet), and name the
   congestion-signal opportunity the design wastes (dup-ACKs).
4. F5: one concrete failure and one security exposure. Patch both.
5. Verdict: ship / fix-then-ship / redesign — with your top three patches ordered.

### Expected learning outcomes
- Derive failure modes from protocol design under stated network conditions.
- Practice design-review discipline: mechanism, trigger, consequence, patch.
- Recognize when a custom protocol is re-deriving TCP (and should stop).

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "A timer is a *model* of the network. What does a 200 ms model get wrong at 150 ms
   RTT — and at 5 ms?"
2. "Two constants (F2, F3) mean the protocol can neither slow down nor speed up. What
   does a fixed 64-packet sender do to everyone else when loss starts?"

### Solution
1. F1 at 150 ms RTT: every packet is retransmitted ~once (timer fires before the ACK
   returns) → ≥2× traffic and duplicate data storms; effective goodput collapses as
   the receiver dedupes. F1 at 5 ms: 200 ms is 40× the needed timeout — *slow* (each
   real loss idles 200 ms), but survivable on LAN. Severity: high (branch) / low
   (LAN). Patch: adaptive timer (RTT-sampled, e.g., SRTT ± 4×RTTVAR, per RFC 6298
   style ⚠) or per-path measurement.
2. F2+F3: on shared loss, FastSync keeps 64 packets in flight, retransmits lost ones
   at fixed rate, and never backs off — it *undermines* TCP's AIMD: while SSH/TCP
   halves its window per loss, FastSync keeps grabbing the freed capacity
   ("congestion-collapse contributor"). Predicted: SSH RTT inflates by tens of ms
   continuously, TCP flows starve relative to FastSync (unfairness), queue builds at
   the uplink (bufferbloat conditions). Severity: high — it damages *other* users'
   traffic by design. Patch: AIMD-style response (halve window on loss, probe upward)
   — i.e., adopt congestion control; the minimal honest patch is "implement slow
   start + multiplicative decrease".
3. F4: individual ACKs = 1:1 ACK:data — 2× packet count at full window (vs cumulative
   ACKs amortizing to ~1 per window). Wasted signal: duplicate ACKs arriving at the
   sender are the classic loss detector; FastSync ignores the *information* (it just
   re-ACKs dupes) while paying full retransmit on timer alone. Patch: cumulative
   ACKs + dup-ACK-count (3⇒ fast retransmit), or SACK-style selective reports if
   out-of-order delivery matters.
4. F5: failure — two senders to the same port interleave into one receive path
   (traffic mixing/corruption of the stream state); exposure — any host on the LAN
   can inject/inject-ACK a stream (spoofed source on UDP; no connection identity ⇒
   no origin check). Patch: per-stream connection ID (random 64-bit) + handshake
   (SYN-style exchange that establishes the ID) + receiver binding to the
   negotiated ID; optionally cryptographic tag if hostile LANs are in scope.
5. Verdict: **fix-then-ship** (not redesign: F1–F4 have local patches; F5 needs a
   handshake bolt-on). Order: (1) congestion response (F3 — harms others today),
   (2) adaptive timer (F1 — breaks branch links), (3) connection ID/handshake (F5 —
   correctness + security). Then cumulative ACKs (F4) as efficiency. If the team
   cannot take on congestion control maintenance, the honest verdict flips to *use
   TCP/quic* — maintaining AIMD is a project, not a patch ⚠ judgment call; say which
   you'd choose for a 4th-semester team and why.

### Reasoning process
Method: for each line — derive mechanism from transport principles, find the trigger
in the deployment list, state the user-visible consequence, patch minimally. Severity
= scope × visibility. Verdict weighs patch count vs redesign cost vs team capacity.
The review's meta-lesson: F2+F3+F4 are convergent evolution toward TCP — recognize it.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "It works on the LAN, ship it" | The deployment target includes 150 ms RTT branch links and a *shared* uplink — the tested environment is the unrepresentative one |
| "Add more buffers at the receiver" | None of F1–F5 is a buffering problem |
| "Just use TCP everywhere" (as the *only* review finding) | Misses the review's teaching goal (deriving failures) — acceptable only as the *verdict* with justification |
| Rating F5 low because "the LAN is friendly" | The deployment target is a shared office uplink; trust boundaries exist exactly where it ships |

### Extension question
QUIC exists. Map FastSync's five flaws onto what QUIC provides for each (timer:
RTT-adaptive loss recovery; window: congestion control built in; ACKs: cumulative +
SACK blocks; handshake + connection ID: cryptographic 1-RTT handshake with connection
IDs designed for migration). Then answer: does knowing QUIC change your verdict for a
4th-semester team? ⚠ (Argue both: maturity argues for QUIC/library; pedagogy argues
for building a toy — the review board's job is to say which goal this project has.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All five lines: mechanism→trigger→consequence→patch; quantified ACK overhead; ordered verdict with team-capacity honesty |
| 3 Proficient | Failures derived for most lines; patches generic |
| 2 Developing | Restates the flaw ("fixed timer is bad") without derived consequences |
| 1 Beginning | "Use TCP" as the only finding |

### References
- Kurose & Ross §3.4–3.7 (reliable transfer + congestion control principles)
- RFC 6298 (RTO computation) ⚠; QUIC: RFC 9000/9002 (transport/loss recovery) ⚠
