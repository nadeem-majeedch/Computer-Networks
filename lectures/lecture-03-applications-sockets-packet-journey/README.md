# Lecture 03 — Applications, Sockets & the First Packet Hunt

| Field | Value |
|---|---|
| Module | 1 — Foundations & Architecture |
| Depends on | L01, L02 |
| CLOs addressed | **CLO1** (primary), CLO4 (first packet work) |
| Bloom level | C2–C3 |
| Assessment artifact | Exit ticket; GA-03 submission (socket demo + request journey) |
| Lab | GA-03a Python socket demo; GA-03b "journey of one HTTP request" |
| Readings | KR §2.1; PD §9.1 (perspective) |
| Prerequisites | L01–L02 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- How does an application program actually *talk* to the network?
- What must two programs agree on before their first byte?
- Where does every packet of a web page load come from, in order, and why?

## What you should be able to do afterwards
- Explain the client/server and P2P models with real examples.
- Describe what a socket is (IP+port) and use it to reason about connections.
- Trace the full journey of one web request across all layers, naming each protocol.
- Predict the packet sequence (DNS → TCP → TLS → HTTP) of a simple page load.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Skim the LAB-01 handout. Come with the course VM working (help desk hours posted).
