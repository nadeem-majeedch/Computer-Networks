# Lecture 19 — TCP Flow & Congestion Control

| Field | Value |
|---|---|
| Module | 4 — Transport Layer |
| Depends on | L18 (seq/ack, RTO, buffers) |
| CLOs addressed | **CLO5, CLO6** (primary), CLO4 (measurement) |
| Bloom level | C4 |
| Assessment artifact | Lab report (LAB-09) with graphs & interpretation |
| Lab | LAB-09: TCP performance under `netem` (delay/loss/bandwidth sweeps) |
| Readings | KR §3.5.5, §3.6–3.7; RFC 5681 (skim); RFC 9293 §3 |
| Prerequisites | L17–L18 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-09 handout (labs/) |

## Key questions
- Why can a receiver with a 64 KB window on a 1 Gbps link only get ~5 Mbps across the
  Atlantic?
- How does TCP *find* the network's capacity without being told — and how does it
  behave when it's wrong?
- What is bufferbloat, and why does a bigger buffer make latency worse?

## What you should be able to do afterwards
- Compute throughput from window and RTT (L·W/RTT) and explain the bandwidth-delay
  product.
- Walk slow start, congestion avoidance, fast retransmit/recovery through a loss event.
- Run controlled degradation experiments (netem) and interpret the resulting curves.
- Explain bufferbloat with queueing math from L01.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-09 handout

## Homework / preparation for next lecture
- LAB-09 report due. Project spec (LAB-10/11) due next session — start now.
