# Lecture 02 — Layered Architectures: OSI & TCP/IP

| Field | Value |
|---|---|
| Module | 1 — Foundations & Architecture |
| Depends on | L01 |
| CLOs addressed | **CLO1** (primary), CLO2 (introduced) |
| Bloom level | C2 |
| Assessment artifact | Exit ticket; encapsulation worksheet (GA-02) |
| Lab | GA-02: header-dissection puzzle on a real frame |
| Readings | KR §1.5; PD §1.4–1.5; RFC 1122 §1 (perspective) |
| Prerequisites | L01 (packets, protocols, Internet structure) |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- Why do we split network software into layers at all — and what does layering cost us?
- What does OSI's 7-layer model *mean* when it isn't a protocol suite?
- How does a single application message become a frame, and how does it become one again?
- Who standardizes what, and how do I read a protocol standard?

## What you should be able to do afterwards
- Explain the purpose of layering and its trade-offs (complexity hiding vs rigidity/overhead).
- Recount OSI 7 layers and the TCP/IP 5-layer view, naming each layer's job and PDU.
- Walk a message down the stack (encapsulation) and up (decapsulation) on a concrete packet.
- Identify the standards body behind a given technology (IEEE 802.3, RFC 9293, …).

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Read KR §2.1 (principles of network applications). Bring one app you use daily and guess
  whether it is client-server or peer-to-peer.
