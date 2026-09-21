# Lecture 23 — Instructor Teaching Notes
## Core Application Protocols: HTTP/1.1 → HTTP/3, SMTP & SSH (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO4 primary; CLO6/CLO7 supporting |
| Textbook anchor | KR §2.2–2.3, §2.5 |

---

## 1. Objectives hook
Board: **"Same web page, three protocols, three captures. The difference isn't features
— it's *who queues behind whom*."**

Hook (2 min): show the three LAB-12 captures side by side (same VM-hosted page):
H/1.1's serial requests, H/2's multiplexed frames, H/3's single UDP "connection" —
the lecture's whole arc in one screenshot triple.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L22 options recall; the capture triple |
| 6–30 | Concept 1 | HTTP core (request/response, methods, codes) + H/1.1's serial problem |
| 30–50 | Concept 2 | H/2 multiplexing; H/3/QUIC: why UDP (L17/L19 payoff) |
| 50–58 | Concept 3 | SMTP transaction (envelope vs headers) |
| 58–63 | Break | — |
| 63–70 | Concept 4 | SSH setup anatomy (banner→algorithms→auth→channel) |
| 70–75 | LAB-12 briefing + CS-03 opening | Handout walk; evidence-log template |
| 75–108 | LAB-12 (in-class) | Captures & dissections, pairs |
| 108–116 | CS-03 kickoff | Brief + bundle-1 (L23) evidence; log expectations |
| 116–120 | Summary + exit ticket | — |

## 3. Concept walkthrough

### 3.1 HTTP core & the serial problem (24 min)
- **Request/response text protocol:** methods (GET/POST/PUT/DELETE semantics —
  RFC 9110), status families (2xx/3xx/4xx/5xx with the famous dozen), headers
  (Host — L03's mystery solved fully: virtual hosting), cookies/state (stateless
  protocol, stateful apps).
- **H/1.0 → H/1.1:** connection per object → **keep-alive** (reuse the TCP connection)
  → **pipelining** (send requests ahead) — which *failed in practice* (head-of-line
  blocking: one slow response stalls the queue) → browsers used parallel
  connections (6-ish) instead — the sharding hack era.
- **Performance math (L19's formula returns):** each new connection pays slow start;
  parallel connections compete and re-train cwnd — H/1.1's real cost isn't bytes,
  it's *windows*. Have students articulate that sentence; it's the module's
  synthesis moment.

### 3.2 H/2 and H/3 (20 min)
- **H/2 (RFC 9113):** binary framing over *one* TCP connection: streams +
  multiplexing (no HOL *between streams at the HTTP layer*), header compression
  (HPACK), server push (now deprecated — mention, don't teach). HOL moves *down*:
  TCP's in-order byte stream (L18!) means one lost segment stalls ALL streams —
  the protocol's own design haunting it.
- **H/3 (RFC 9114) over QUIC (RFC 9000):** streams built *inside* the transport on
  UDP: per-stream loss recovery (no cross-stream HOL), TLS 1.3 baked into the
  handshake (1-RTT initial, 0-RTT resumption), connection *migration* (connection
  IDs survive IP changes — the Wi-Fi→5G walk survives).
- **The arc as an evaluation argument (CLO6):** H/1.1 HOL at app layer → H/2 HOL at
  TCP layer → H/3 fixes it at transport. Students can now *name the layer of every
  bottleneck* — the layered model (L02) paying its dividend.

### 3.3 SMTP (8 min)
- **Envelope vs headers:** MAIL FROM/RCPT TO (envelope — what servers use) vs
  From:/To: (headers — what humans see); the spam-era distinction with teeth.
- **Transaction:** EHLO → MAIL FROM → RCPT TO → DATA → (headers, blank line, body,
  `.`) → QUIT; status codes (250/354/550) echo FTP-era style; submission (587,
  auth) vs relay (25) ports; SPF/DKIM/DMARC named (TXT records — L21's payoff).
- Simplified flag: modern SMTP is extension-negotiated (EHLO verbs: STARTTLS,
  AUTH, SIZE); we teach the core transaction shape.

### 3.4 SSH anatomy (7 min)
- **Why SSH looks "quiet" in captures:** binary, encrypted from early on.
  Phases: TCP connect → **banner** (`SSH-2.0-...` plaintext!) → algorithm
  negotiation (KEXINIT: key exchange, ciphers, MACs) → key exchange → encrypted
  auth (password/public-key — the capture shows *sizes*, not secrets) →
  **channels** (one connection, many sessions: shell, forwarding).
- L24's TLS handshake will feel familiar — same negotiation shape; SSH is the
  second witness that "secure protocol = negotiate, authenticate, then speak
  encrypted" is a *pattern*, not a one-off.

### Reference diagram — HTTP/1.1 request/response

```text
client                                     server
   │──── GET /index.html HTTP/1.1 ─────────────→│
   │←─── 200 OK + body ─────────────────────────│  HTTP/1.1 reuses
   │──── GET /logo.png HTTP/1.1 ───────────────→│  the TCP connection
```

## 4. Important definitions
Method/status code · Keep-alive · Pipelining · Head-of-line blocking (app vs
transport layer) · Stream/frame · Multiplexing · HPACK (named) · QUIC connection
ID / migration · 0-RTT (named) · Envelope vs headers · Submission vs relay ·
SPF/DKIM/DMARC (named) · KEXINIT · Channel (SSH) · Banner.

## 5. Real-world examples
- **"Page of 100 images"** across the three protocols — the classic demo: same
  bytes, wildly different completion curves (LAB-12 reproduces it locally).
- **"My upload stalls when one request is slow"** — H/1.1 HOL wearing a support
  ticket; knowing the layer names the fix (upgrade path).
- **Email deliverability** = SPF/DKIM/DMARC alignment — the DNS TXT records from
  L21 doing a security job (thread connect).

## 6. Mathematical/technical example
H/1.1 vs H/3 for a 50-object page, 40 ms RTT, 2% loss: H/1.1 (6 parallel conns,
slow start each) vs H/2 (one conn; loss stalls all streams: ×RTT recovery) vs H/3
(per-stream recovery: only the affected stream pauses). Students estimate with the
L19 formula + L18's dup-ACK knowledge — quantitative synthesis, not hand-waving.
(Numbers approximate; the *shape* of the comparison is the assessed skill.)

## 7. LAB-12 briefing (5 min)
Locally hosted test page (the VM image ships one ⚠ verify): capture H/1.1 (force via
`curl --http1.1`), H/2 (`curl --http2`), H/3 (`curl --http3` if built; else provided
capture), SMTP (VM mail service handout), SSH (banner + KEXINIT visible pre-encryption).
Worksheet: identify HOL evidence per version; decode one SMTP transaction; SSH banner
+ algorithms. ⚠ Verify curl HTTP/3 support on the image — if absent, the provided
capture is the graded path (state this in the handout).

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "HTTP/2 fixed slow websites" | It moved HOL to TCP; loss-heavy paths can regress — that's why H/3 exists |
| "QUIC is 'UDP with encryption'" | It's a *transport* (streams, reliability, congestion control) rebuilt over UDP |
| "SMTP headers = envelope" | Servers route on envelope; headers are display + anti-spam evidence |
| "SSH on port 22 means unencrypted negotiation only" | Only the banner is plaintext; KEXINIT is part of setup *by design* (algorithms before secrets) |
| "0-RTT is free speed" | Replay risk; TLS 1.3 fences it (L24) |
| "Server push is core H/2" | Deprecated in practice; H/3 dropped it — teach the *frame model*, not push |

## 9. Suggested practical demonstration
The capture triple (§1 hook) expanded: filter each capture to show requests per
connection; then H/2 frames (Wireshark's `http2.stream` filter) and H/3 QUIC frames.
5 minutes before LAB-12. ⚠ Pre-verify image tooling (curl variants) or use provided
captures.

## 10. Classroom activities
- **HOL relay:** one "TCP" student must hand bytes in order to three "stream"
  students; drop one packet in the middle — every stream freezes. Then re-run as
  three QUIC channels. The lecture's thesis, physicalized.
- **SMTP play-by-play:** two volunteers run the transaction with envelope/header
  cards; a third tries to spoof From: — envelope wins; DKIM foreshadowed.

## 11. Problem-solving questions
1. Why did pipelining fail in H/1.1 while H/2 multiplexing succeeded?
2. A capture shows one TCP connection carrying interleaved objects — which HTTP
   version, and which frame field tells you?
3. Envelope From: `a@x.com`, header From: `ceo@bank.com` — what does the receiving
   server do with each? (routing vs display/anti-spoof)
4. Why does QUIC survive a Wi-Fi→5G switch mid-transfer? (connection IDs)
5. Where does HOL *still* exist in H/3? (QUIC packet-level recovery across streams
   on the same datagram path — nuance, name it honestly)

## 12. Formative assessment (with answers)
- MCQ: H/2's HOL lives in → **TCP's in-order stream**.
- MCQ: SMTP routing uses → **the envelope (MAIL FROM/RCPT TO)**.
- MCQ: SSH's plaintext banner exists to → **version exchange before protocol setup**.
- Short: one transport problem H/3 fixes and how. → per-stream loss recovery via
  QUIC streams over UDP (no cross-stream HOL).

## 13. Exit ticket
1. HOL locations: H/1.1 at ________; H/2 at ________; H/3 fixes via ________
2. Envelope commands (two): ________
3. SSH's setup order: banner → ________ → ________ → channels.

## 14. Anticipated difficulties
- Students conflate HTTP/2 (TCP) and HTTP/3 (QUIC) *because both say
  "multiplexing"* — the layer-of-HOL question is the discriminator; drill it.
- LAB-12's HTTP/3 capture depends on tooling (⚠ curl build) — the handout's
  provided-capture fallback must be ready before class.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify curl H/2 & H/3 support + local test page on the image
- [ ] Pre-build the three captures; SMTP/SSH demo services running
- [ ] Print LAB-12 + CS-03 evidence-log templates; Meridian bundle-1 staged
- [ ] Board pre-write: HOL-arc diagram; SMTP transaction skeleton; SSH phases

## 16. Timing fallbacks
SSH section can shrink to the banner+negotiation shape (3 min); the HOL arc and
LAB-12 captures are protected; CS-03 kickoff must keep ≥8 minutes (bundle-1 needs
framing).

## 17. References
- KR §2.2–2.3, §2.5; RFC 9110/9112 (HTTP), RFC 9114 (H/3), RFC 9000 (QUIC),
  RFC 5321 (SMTP), RFC 4251-4253 (SSH family), RFC 7469/6376/7208 (DMARC/DKIM/SPF,
  named).
- Wireshark HTTP/2 & QUIC dissector docs; curl docs; LAB-12 handout.
- ⚠ VERIFY editions/sections and image tooling this semester.
