# Weekly Quiz — Week 10 (L19, L20)

| Field | Value |
|---|---|
| Coverage | L19 — TCP flow & congestion control · L20 — Reliable transport over UDP (project) |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | **Graded-quiz candidate window** (strategy §2; see assessments/README.md §5 reconciliation note) |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO4|L19]** Distinguish flow control from congestion control in one sentence
each, naming the signal each uses.

**Q2 [I|CLO5|L19]** Compute the bandwidth–delay product of a 100 Mb/s path with 50 ms
RTT, in kilobytes. What buffer size does the receiver need to keep the pipe full?

**Q3 [I|CLO4|L19]** In slow start, cwnd doubles per RTT. Starting at 1 MSS with RTT =
40 ms, how long until cwnd ≥ 16 MSS (in MSS units per RTT, no loss)?

**Q4 [I|CLO4|L19]** After a timeout, TCP sets ssthresh and re-enters slow start. Given
cwnd = 20 MSS at loss with ssthresh = 16, state the post-loss cwnd and ssthresh using
the course's simplified rules.

**Q5 [I|CLO5|L20]** Your reliable-UDP protocol uses seq numbers + cumulative ACKs +
RTO retransmit. Which TCP-style behavior have you *not* yet implemented if a single lost
segment still blocks all later data at the receiver? Name it and sketch the fix.

**Q6 [I|CLO6|L20]** Your transfer over a 20 ms path reaches only 5 Mb/s despite a
100 Mb/s link and loss-free ping. Using throughput ≈ window/RTT, what window does the
observed rate imply, and what does that suggest was limiting?

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Flow control protects the *receiver*: receiver-advertised window (rwnd).
Congestion control protects the *network*: sender-side congestion window (cwnd) reacting
to loss/delay signals. Effective limit is min(cwnd, rwnd). [B·CLO4]

**Q2.** BDP = 100×10⁶ b/s × 50×10⁻³ s = 5×10⁶ bits = 625 000 bytes = **≈ 625 kB**
(610 KiB acceptable) [MC]. To keep the pipe full, in-flight data ≈ BDP, so the receiver
window must be at least that. [I·CLO5]

**Q3.** 1→2→4→8→16: doubling each RTT reaches 16 MSS after **4 RTTs = 160 ms** [MC]. [I·CLO4]

**Q4.** ssthresh ← max(cwnd/2, 2) = **10 MSS**; cwnd resets to **1 MSS** and slow start
re-runs (course's simplified RFC-5681-style rule; accepting cwnd=1 + halved ssthresh
with correct reasoning). [I·CLO4]

**Q5.** Missing **selective acknowledgment/out-of-order buffering**: TCP's cumulative
ACK alone would also stall, but real TCP buffers out-of-order data and (SACK) reports
gaps, letting the sender retransmit just the hole. Fix for the protocol: buffer
out-of-order segments at the receiver and ACK/selectively NAK the missing seq so later
segments aren't discarded. [I·CLO5]

**Q6.** window ≈ throughput × RTT = 5×10⁶ × 20×10⁻³ = 100 000 bits = **12.5 kB** [MC].
A ~12.5 kB window on a loss-free path is far below BDP (250 kB) → the *window* (or app
send pattern), not bandwidth or loss, was the limiter. [I·CLO6]
