# Lecture 18 — TCP Essentials: Connections & Reliable Delivery

| Field | Value |
|---|---|
| Module | 4 — Transport Layer |
| Depends on | L17 (transport jobs, demux), L12 (IP model) |
| CLOs addressed | **CLO4** (primary), CLO5 (measurement preview) |
| Bloom level | C2–C4 |
| Assessment artifact | Exit ticket; annotated trace excerpt (GA-18) |
| Lab | GA-18: handshake & retransmission dissection on a real trace |
| Readings | KR §3.5.1–3.5.4; RFC 9293 (skim §3) |
| Prerequisites | L17 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- What *is* a TCP connection, physically and logically?
- How do sequence numbers turn an unreliable IP service into ordered, complete bytes?
- What exactly happens when a segment is lost, and what does the receiver do?

## What you should be able to do afterwards
- Explain the 3-way handshake and connection teardown with sequence-number arithmetic.
- Predict acknowledgment numbers for simple exchange sequences.
- Recognize retransmissions, duplicate ACKs, and RST in a capture.
- Explain buffers, MSS, and why segment size is 1460 on Ethernet.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-18. Read KR §3.5.5, §3.6–3.7 (flow/congestion control).
