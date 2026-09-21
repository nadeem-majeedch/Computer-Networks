# Lecture 23 — Core Application Protocols: HTTP/1.1 → HTTP/3, SMTP & SSH

| Field | Value |
|---|---|
| Module | 5 — Application Layer & Network Services |
| Depends on | L03 (journey), L17–L19 (transport), L21 (DNS), TLS usage is a forward preview only (covered in Module 6 — not a dependency) |
| CLOs addressed | **CLO4** (primary), CLO6 (protocol comparison), CLO7 (security usage thread) |
| Bloom level | C3–C4 |
| Assessment artifact | Lab worksheet (LAB-12); **CS-03 opens** (evidence log) |
| Lab | LAB-12: capture & compare HTTP/1.1 vs HTTP/2 vs HTTP/3; SMTP & SSH dissection |
| Readings | KR §2.2–2.3, §2.5; RFC 9110/9112 (skim); RFC 5321 (skim) |
| Prerequisites | L17–L19, L21 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-12 handout (labs/) |

## Key questions
- How did the web's protocol evolve from one-request-per-connection to multiplexed
  streams over QUIC — and what *transport-layer* problems did each step fix?
- What does a mail server conversation look like on the wire?
- Why does SSH look so different from HTTP in a capture?

## What you should be able to do afterwards
- Explain HTTP/1.1 → /2 → /3 evolution via head-of-line blocking at each layer.
- Read HTTP methods/status codes and connect keep-alive/multiplexing to L19's math.
- Walk an SMTP transaction and SSH's setup (banner, algorithms, auth, channel).
- Open CS-03's evidence log from Meridian's outage materials.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-12 handout

## Homework / preparation for next lecture
- LAB-12 worksheet due. CS-03 evidence log opened per the case-study brief.
- Read KR §8.1–8.3 — security foundations next.
