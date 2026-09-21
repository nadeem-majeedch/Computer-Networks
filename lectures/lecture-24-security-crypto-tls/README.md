# Lecture 24 — Security Principles & Cryptographic Building Blocks

| Field | Value |
|---|---|
| Module | 6 — Network Security |
| Depends on | L11 (security thread), L21 (DNS security), L23 (SSH pattern) |
| CLOs addressed | **CLO7** (primary), CLO4 (TLS dissection) |
| Bloom level | C3–C4 |
| Assessment artifact | Exit ticket; certificate-chain + TLS worksheet (GA-24) |
| Lab | GA-24: read a real certificate chain; TLS handshake dissection |
| Readings | KR §8.1–8.3, §8.5; RFC 8446 (TLS 1.3, skim) |
| Prerequisites | L11, L23 |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) · slides.md (pending later pass) |

## Key questions
- What does "secure" actually mean — which of secrecy, integrity, and authenticity
  does each mechanism provide?
- How do symmetric and asymmetric crypto *combine* in a real protocol?
- What does the TLS handshake prove, and to whom?

## What you should be able to do afterwards
- Map CIA goals to mechanisms (encryption/MAC/signature) without confusing them.
- Explain why hybrid encryption exists (key distribution vs speed).
- Read a certificate chain: who signs whom, what the SAN names say.
- Walk a TLS 1.3 handshake shape and name what each flight accomplishes.

## Materials
- [Teaching notes](notes.md) · [Worksheet](worksheet.md)

## Homework / preparation for next lecture
- Complete GA-24. Read KR §8.4 (firewalls intro) — defenses next.
