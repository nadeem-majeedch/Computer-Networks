# Lecture 06 — Data Link Layer: Framing, Errors & Reliability

| Field | Value |
|---|---|
| Module | 2 — Physical & Data Link Foundations |
| Depends on | L05 (signals/media), L02 (PDU concept) |
| CLOs addressed | **CLO2** (primary) |
| Bloom level | C3 |
| Assessment artifact | Exit ticket; GA-06 CRC worksheet (computed by hand) |
| Lab | GA-06 (in-lecture); no numbered lab |
| Readings | PD §2.4–2.5; Tanenbaum data-link chapter (⚠ verify section) |
| Prerequisites | L05; comfort with binary and polynomial arithmetic basics |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- How does a receiver find the start and end of a frame inside a bit stream?
- How do you detect that a bit got flipped — with 1 bit, with 16 bits, with a polynomial?
- When should errors be corrected at the link, and when simply retransmitted?

## What you should be able to do afterwards
- Explain framing with byte stuffing and bit stuffing, and compute stuffed frames.
- Compute a CRC remainder by polynomial division for a small message.
- Choose between parity, checksum, CRC, and FEC for a given scenario, with justification.
- Explain why Ethernet kept error *detection* but delegated error *recovery* upward.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Read PD §2.6 (Ethernet). Bring one question about MAC addresses.
