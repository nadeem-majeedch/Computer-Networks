# Weekly Quiz — Week 12 (L23, L24)

| Field | Value |
|---|---|
| Coverage | L23 — HTTP/2 & HTTP/3, SMTP, SSH · L24 — Security principles & cryptographic building blocks |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | **Graded-quiz window per syllabus/schedule (Quiz 2)** — see assessments/README.md §5 reconciliation note |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO4|L23]** State the one transport change HTTP/3 makes versus HTTP/2, and the
performance problem it removes.

**Q2 [I|CLO4|L23]** SMTP is a push protocol with store-and-forward relays. Give one
consequence for delivery *timing* and one for *authentication* that email still wrestles
with today.

**Q3 [B|CLO7|L24]** Map each goal to the CIA triad letter: (i) an intruder cannot read
database dumps, (ii) logs prove who approved a change, (iii) attackers cannot alter
in-flight balances.

**Q4 [I|CLO7|L24]** Why does TLS use asymmetric crypto only to *establish* a session,
then switch to symmetric keys? One sentence for the "why asymmetric" and one for the
"why symmetric afterward."

**Q5 [I|CLO7|L24]** What does a hash function give you that encryption does not, and
what property makes it usable for integrity checks?

**Q6 [I|CLO7|L24]** A certificate warning says the server's certificate was signed by
"Unknown Authority." Explain, in chain-of-trust terms, what failed and one legitimate
situation where this is expected.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** HTTP/3 runs over **QUIC over UDP** instead of TCP; it removes TCP head-of-line
blocking (one lost stream no longer stalls all streams) and folds transport+crypto
handshake into fewer round trips. [B·CLO4]

**Q2.** Timing: mail may sit in relays/queues for minutes-to-days, so delivery is not
interactive. Authentication: SMTP itself authenticates nothing about the sender — hence
deployed add-ons (SPF/DKIM/DMARC) and persistent spoofing problems. [I·CLO4]

**Q3.** (i) Confidentiality (C) · (ii) Accountability/non-repudiation — maps to the
auditing pillar (accept "A for accountability/availability debate" only with the
audit-trail justification; the course's triad usage is C/I/A + accountability) ·
(iii) Integrity (I). [B·CLO7]

**Q4.** Asymmetric: lets two parties who share no secret establish one over an open
channel and authenticate the server's certificate. Symmetric afterward: bulk crypto is
vastly faster per byte, so the expensive public-key work is done once per session. [I·CLO7]

**Q5.** A hash gives a fixed-length *fingerprint* without any key — you can compare
digests without decrypting anything. Collision/preimage resistance means any change to
the input changes the digest, so comparing digests detects tampering. [I·CLO7]

**Q6.** Chain-of-trust validation failed: the certificate is not signed by any CA the
client trusts (no anchor in the trust store), so authenticity is unproven. Legitimate
cases: internal/self-signed appliances, or a private corporate CA not installed on that
client — ⚠ the browser's warning is still correct behavior for the client. [I·CLO7]
