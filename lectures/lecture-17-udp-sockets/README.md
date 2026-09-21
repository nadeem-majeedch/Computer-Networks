# Lecture 17 — UDP & the Transport Layer's Job

| Field | Value |
|---|---|
| Module | 4 — Transport Layer |
| Depends on | L12 (IP model), L03 (sockets as an app concept) |
| CLOs addressed | **CLO4, CLO5** (primary), CLO6 (protocol-choice reasoning) |
| Bloom level | C3 |
| Assessment artifact | Working UDP chat/file-transfer demo (LAB-08) |
| Lab | LAB-08: build a UDP chat/file-transfer client & server (Python, pairs) |
| Readings | KR §3.1–3.3; RFC 768; RFC 8085 (usage guidance, skim) |
| Prerequisites | L12; Python basics (L03) |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-08 handout (labs/) |

## Key questions
- Why does the transport layer exist at all — what jobs does IP refuse to do?
- What does UDP add to IP, exactly (8 bytes of header), and why is that enough for
  DNS, streaming, and games?
- When should an application choose UDP — and then fix what UDP doesn't fix?

## What you should be able to do afterwards
- Explain multiplexing/demultiplexing by ports, with the demux keys of UDP and TCP.
- Read a UDP header from a capture and validate the length field.
- Build a working UDP client/server and reason about loss, reordering, duplication.
- Argue the UDP-vs-TCP choice for a given application with three criteria.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md) · LAB-08 handout

## Homework / preparation for next lecture
- LAB-08 demo due. Read KR §3.5.1–3.5.4 (TCP basics) — TCP week begins.
