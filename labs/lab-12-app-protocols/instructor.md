# LAB-12 — Instructor Guide

## Setup (before session)
- **Capture the offline bundle yourself** from the teaching image: the five files named in
  the README. SMTP: run a local postfix/exim on a lab VM with synthetic addresses — never
  capture real user mail. SSH: scripted login, password redacted in the capture ⚠ verify
  before distributing.
- ⚠ Endpoint caveat (lab-strategy §7): `neverssl.com` and `cloudflare-quic.com` are
  teaching conveniences, not guarantees — re-test each semester and refresh the bundle.
  The image ships a local plain-HTTP fallback; document its URL in the session notes.

## Solutions / expected values
- **Pre-lab 1:** keep-alive reuses the TCP connection serially; multiplexing interleaves
  frames concurrently on one connection.
- **Pre-lab 2:** QUIC/UDP; setup + crypto handshake are one flow; no kernel retransmits
  (QUIC does its own).
- **Pre-lab 3:** cert proves the server's identity to the client (chain to a trusted CA).
- **T1:** readable GET; the three-object arithmetic (post-lab 1): 3×(handshake + TLS 1-RTT)
  vs 1×(handshake + TLS) + multiplexed requests — RTT multiples from LAB-01 habits.
- **T2:** ALPN: `h2` in the TLS extension; binary frames (HEADERS/DATA) in tshark output.
- **T3:** UDP 443 flow, QUIC Initial; zero TCP SYN anywhere for the same fetch.
- **T4:** subject/issuer/dates; expiry breaks trust verification — browsers block, sites
  break (chain order from `-brief`).
- **T5:** SMTP commands/responses fully visible pre-STARTTLS (none in the teaching capture);
  SSH: cleartext banner + KEX, then binary encrypted packets; auth payload invisible.

## Common failure modes
1. Students fetch HTTPS for T1 and conclude "HTTP is encrypted" — enforce the plain-HTTP
   target for T1 (that's the pedagogical point).
2. Cert date confusion (valid *from* in future on some CDNs) — read `-dates` carefully.
3. Treating the bundle as "second class" — rubric is identical for bundle-based reports.

## Grading notes
- Correct results (40): annotation tables T1/T2/T5 + chain fields T4.
- Analysis (30): post-lab 1 arithmetic + post-lab 2 QUIC re-implementations.
- Reproducibility (20): bundle files cited OR live captures with commands.
- Clarity (10): endpoint failures honestly noted (they will happen — reward the note).
