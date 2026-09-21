# Lecture 24 — Instructor Teaching Notes
## Security Principles & Cryptographic Building Blocks (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO7 primary; CLO4 supporting |
| Textbook anchor | KR §8.1–8.3, §8.5; RFC 8446 |

---

## 1. Objectives hook
Board: **"Encryption, hashing, signatures, MACs, certificates — five words this course
has used loosely all semester. Today they become precise tools with exact jobs."**

Hook (2 min): poll — "HTTPS protects you from which of: your ISP reading your
traffic / your ISP *modifying* it / a fake bank site / malware on your laptop?"
(The third answer is the lecture; the fourth is the honest boundary.)

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | Thread recap (L11/L21/L23 security sightings); the poll |
| 6–24 | Concept 1 | CIA triad; threat taxonomy; crypto goals vs tools mapping |
| 24–44 | Concept 2 | Symmetric vs asymmetric; hybrid encryption; hash→MAC→signature |
| 44–55 | Concept 3 | PKI: certificates, chains, trust anchors, revocation (concept) |
| 55–60 | Break | — |
| 60–78 | Worked example | TLS 1.3 handshake flight-by-flight (diagram + capture) |
| 78–100 | GA-24 | Certificate chain reading + handshake dissection, pairs |
| 100–112 | Discussion | What HTTPS does NOT protect (poll revisited with precision) |
| 112–118 | Summary + exit ticket | — |
| 118–120 | Preview | Firewalls/VPN/IDS next |

## 3. Concept walkthrough

### 3.1 Goals, threats, tools (18 min)
- **CIA triad:** Confidentiality (only principals can read), Integrity (no
  undetected modification), Availability (service survives attack) — availability
  gets its own lecture (L26's DoS workshop) but belongs in the triad.
- **Threat taxonomy (the course's accumulated sightings, now classified):**
  eavesdropping (L11 Wi-Fi), spoofing/impersonation (L12 ARP, L21 DNS, L22 DHCP),
  MITM (the composite attack), replay (L23's 0-RTT), DoS (L18 SYN flood, L22
  starvation).
- **Tool↔goal mapping (the table students must own):**
  | Goal | Tool | Property |
  |---|---|---|
  | Confidentiality | Symmetric encryption (AES) | Fast; key-sharing problem |
  | Integrity + authenticity (message) | MAC (HMAC) | Shared key; fast |
  | Integrity + authenticity (public) | Digital signature | Private key signs; anyone verifies |
  | Tamper evidence (one-way) | Hash (SHA-256) | No key; not secrecy — collisions computationally infeasible |
- The classic confusion to kill: **hashing is NOT encryption** (no key, no
  reversal); **signing is NOT "encrypting with the private key"** (RSA's textbook
  coincidence — modern schemes like Ed25519 have no such reading; teach concepts
  with named algorithms, no math derivations).

### 3.2 Symmetric vs asymmetric & hybrid (20 min)
- **Symmetric:** one shared key; ~10³× faster; the *problem* is distribution
  ("how do we share the secret without meeting?").
- **Asymmetric (RSA/ECDH/EdDSA families, named):** keypair; public key published;
  solves distribution but slow → **hybrid pattern (the answer to both):**
  1. Use asymmetric (Diffie–Hellman) to *agree* on a fresh session key
     (forward secrecy: the long-term key never encrypts data — compromise of it
     later can't unlock past captures).
  2. Use symmetric for the bulk traffic.
- **DH in three sentences (no math):** two parties mix colors publicly, keep
  secrets privately, both derive the same mixture an observer can't. Named:
  ECDHE is what TLS 1.3 uses (ephemeral = forward secrecy).
- **Authentication of the exchange:** DH alone is anonymous (MITM-able) — hence
  certificates, next segment.

### 3.3 PKI & certificates (17 min)
- **Certificate = identity + public key, signed by an issuer.** Fields: subject,
  issuer, validity, **SAN** (what browsers actually check — the name list),
  signature algorithm.
- **Chain of trust:** leaf ← intermediate(s) ← root (OS/browser trust store = the
  anchor set). "Who vets the vetters" — governance aside (CA/Browser Forum,
  named, one sentence).
- **What's signed (precisely):** the issuer's signature covers the certificate's
  content — swap a byte, signature breaks (hash inside, of course).
- **Revocation (concept level):** CRL/OCSP named, honest limitations noted
  (soft-fail in practice); certificate transparency (L24-enr) named.
- **Trust store compromise = game over** (the honest boundary; ties to the poll's
  malware answer).

### 3.4 TLS 1.3 flight-by-flight (18 min, worked example)
Diagram + capture (GA-24 uses the same trace):
1. **ClientHello:** supported ciphers, **key_share** (DH material, early!), SNI
   (the name — plaintext, privacy caveat).
2. **ServerHello + {EncryptedExtensions, Certificate, CertificateVerify,
   Finished}:** server picks cipher, sends chain, **CertificateVerify** signs the
   handshake transcript (binding the cert to this session), secrets derive.
3. **Client Finished; application data.** **1-RTT** (vs 1.2's 2-RTT+ — evolution
   framing); **0-RTT** resumption data (replay-fenced — L23's caveat lands).
- **The pattern (with SSH from L23 as witness):** negotiate → authenticate →
  derive → speak symmetric-encrypted. State it as the *secure-protocol template*.

### Reference diagram — TLS 1.3 handshake (1-RTT)

```text
client                                     server
   │──── ClientHello + key share ───────────────→│
   │←─── ServerHello, {cert}, Finished ──────────│  {…} = encrypted
   │──── {Finished}, app data ──────────────────→│  keys in flight 1
```

## 4. Important definitions
CIA triad · Eavesdropping/spoofing/MITM/replay/DoS (classified) · Symmetric vs
asymmetric · Hybrid encryption · DH/ECDHE (concept) · Forward secrecy · Hash ·
MAC/HMAC · Digital signature · Certificate (subject/issuer/SAN) · Chain of trust ·
Trust store · Root CA · CRL/OCSP (named) · ClientHello/Key share · SNI ·
CertificateVerify · Transcript binding · 1-RTT/0-RTT.

## 5. Real-world examples
- **Wi-Fi login page breakage on captive networks** — TLS blocks interception;
  networks must allowlist — the "why can't I see the portal" story from the
  encryption side.
- **The padlock ≠ trustworthy site:** certificate proves *key ownership for that
  name*, not honesty of the owner — the poll's third answer refined.
- **Let's Encrypt** made certificates free/automated — deployment friction was the
  web's encryption bottleneck; governance+engineering combined.

## 6. Mathematical/technical example
Key-size intuition (no math): symmetric AES-128 vs RSA-2048 "equivalent security" —
asymmetric keys are *mathematically structured* objects, so their sizes aren't
comparable bit-for-bit; a table (AES-128 ≈ RSA-3072-ish ballpark, cite current
guidance ⚠) + the punchline: that's *why* hybrid. Hash-chain arithmetic: changing
one byte in a 1 GB file changes the hash completely (avalanche) — integrity at
zero bandwidth cost.

## 7. GA-24: certificates + handshake (22 min)
(a) Provided certificate chain (course VM serves one): read subject/issuer/SAN;
draw the chain; identify the anchor. (b) TLS 1.3 capture: label ClientHello
key_share, mark the encryption boundary, find CertificateVerify, count RTTs.
Answer key: instructor copy. ⚠ Pre-verify the VM's TLS server + capture; browser
capture fallback documented in the handout.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Encryption = security" | Which CIA goals? Availability untouched; endpoints unencrypted (the poll) |
| "Hashing is encryption" | No key, one-way; different tool class |
| "HTTPS encrypts everything including the domain" | SNI plaintext (ECH named as the evolving fix ⚠) |
| "The padlock means the site is safe" | Key ownership for the name; not honesty |
| "Certificates expire because of money" | Validity windows limit exposure of stale identity assertions; automation made short lives cheap |
| "TLS 1.3 removed handshakes" | It *compressed* them; the flights exist (capture proves) |

## 9. Suggested practical demonstration
Live: `openssl s_client -connect <vm-host>:443 -brief` projected — chain in 5
lines; then Wireshark's TLS filter on the GA-24 trace. Two views, one story. ⚠
Pre-verify openssl version output shape; keep the capture as fallback.

## 10. Classroom activities
- **Goal/tool sorting cards:** 12 scenario cards ("prove this file wasn't
  altered", "hide this from the ISP"...) → tool each; races + debate on the two
  genuinely ambiguous ones (teaching moment).
- **Chain-building humans:** 3 students (root/intermediate/leaf) sign cards; an
  "attacker" tries to inject a fake leaf — the trust anchor holds or falls.

## 11. Problem-solving questions
1. Bank site: which mechanisms give (a) secrecy (b) server authenticity (c)
   integrity? Map to tools.
2. Why can't the server just encrypt everything with its *private* key and call
   it secure?
3. Your trust store is compromised. Which attacks become possible? (any name
   spoofing — the honest boundary)
4. What does CertificateVerify bind that the certificate alone doesn't? (this
   session's transcript — anti-MITM)
5. 0-RTT: why the replay fence? (early data can't prove freshness)

## 12. Formative assessment (with answers)
- MCQ: Forward secrecy means → **past sessions stay sealed if the long-term key
  leaks later**.
- MCQ: The browser checks → **SAN names**.
- MCQ: A MAC provides → **integrity + authenticity with a shared key**.
- Short: why hybrid? → asymmetric solves distribution, symmetric carries bulk;
  combine for both.

## 13. Exit ticket
1. CIA: A is protected by (not crypto): ________
2. The secure-protocol template's four steps: ________
3. CertificateVerify signs the ________; it defeats ________.

## 14. Anticipated difficulties
- Crypto math anxiety: promise and *keep* the no-derivations rule; named
  algorithms + properties only (the course's earlier layers did the same with
  TCP constants).
- The poll's precision (what HTTPS does NOT do) can unsettle students who've
  said "HTTPS is secure" all semester — treat as the lecture's success moment,
  not a correction of failure.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify VM TLS server + `openssl s_client` output; GA-24 capture ready
- [ ] Print worksheets + card sets; chain-cards for the activity
- [ ] Board pre-write: goal/tool table; hybrid diagram; handshake flights
- [ ] Current guidance for key-size table (⚠ one sourced slide)

## 16. Timing fallbacks
Compress revocation to one sentence (named, honest limits); GA-24 and the
flight-by-flight are protected — both are the CLO7 anchor and quiz-2 material.

## 17. References
- KR §8.1–8.3, §8.5; RFC 8446 (TLS 1.3); RFC 5280 (X.509/PKI, concept citation);
  RFC 6962 (certificate transparency, named).
- OpenSSL docs (demo tooling); NIST key-size guidance (⚠ cite current edition).
- ⚠ VERIFY editions/sections and tooling this semester.
