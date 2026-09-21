# Lecture 18 — Instructor Teaching Notes
## TCP Essentials: Connections & Reliable Delivery (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO4 primary; CLO5 preview |
| Textbook anchor | KR §3.5.1–3.5.4; RFC 9293 |

---

## 1. Objectives hook
Board: **"The wire loses 1% of packets, reorders some, duplicates others. TCP hands your
browser a perfect byte stream anyway. What is the machinery?"**

Hook (2 min): unplug the network *mid-download* for 3 seconds — the transfer resumes.
"The bytes came back. Today: from where, and who decided?"

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | UDP ladder recall; the unplug story |
| 6–26 | Concept 1 | Segment structure, seq/ack arithmetic, buffers & MSS |
| 26–46 | Concept 2 | Handshake & teardown; state machine highlights |
| 46–60 | Concept 3 | Reliability: RTT estimation, timeout, retransmission triggers |
| 55–60 | Break | (placed inside concept 3 flow) |
| 60–80 | GA-18 | Trace dissection: handshake + retransmission, pairs |
| 80–95 | Worked example | Ack-number arithmetic worksheet on board |
| 95–110 | Discussion | RST vs FIN; what the capture shows when servers die |
| 110–118 | Summary + exit ticket | — |
| 118–120 | Preview | Flow & congestion control (L19) — "the window is coming" |

## 3. Concept walkthrough

### 3.1 Segments, bytes, buffers (20 min)
- **TCP = connection-oriented, byte-stream, point-to-point, full-duplex, reliable.**
  "Connection" = **state at both endpoints** (L03 said it; now precise: sequence
  counters, buffers, window sizes, timers, options).
- **Segment = the PDU.** Key header fields: src/dst ports (L17's demux), **Sequence
  Number** (byte offset of this segment's first data byte), **Acknowledgment Number**
  (next byte expected — *cumulative* ACK), flags (SYN/FIN/ACK/RST/PSH/URG), Window
  (flow control — L19), checksum (L17), options (MSS, SACK, timestamps, window scale).
- **MSS on Ethernet:** 1500 − 20 (IP) − 20 (TCP) = **1460** — the number explains
  L12's efficiency math. Path-MTU discovery adjusts it (L15's v6 note connects).
- **Buffers:** send buffer (app writes → kernel sends as windows allow); receive
  buffer (kernel reorders/holds for the app). "TCP is a pipe with valves" — valves
  are windows (L19).
- Simplified-model flag: we teach sequence arithmetic with small numbers; real stacks
  add random ISNs (security — correct the "seq=0 starts" textbook simplification),
  timestamps, SACK for selective recovery.

### 3.2 Handshake & teardown (20 min)
- **3-way:** SYN (seq=x, own ISN, offers options: MSS, window scale, SACK) →
  SYN-ACK (seq=y, ack=x+1) → ACK (ack=y+1, may carry data). Why three? Both sides
  must *learn each other's ISNs and agree both directions are open*; two would leave
  one direction unacknowledged; the third also carries the first data usually.
  - SYN flood attack named (L26 workshop dissects): half-open connections consume
    state → backlog exhaustion.
- **Teardown:** FIN (half-close: "I'm done sending; I can still receive") → ACK →
  FIN → ACK; 4 packets conceptually, often combined. **RST** = abort (no graceful
  state): port not listening ("connection refused"), mid-path kills, firewalls.
- **States (highlight only):** LISTEN, SYN-SENT, SYN-RCVD, ESTABLISHED,
  FIN-WAIT-1/2, CLOSE-WAIT, LAST-ACK, TIME-WAIT (2×MSL — why it exists: late
  duplicates must die; the state `ss`/`netstat` shows, bridging to LAB-01 tooling).

### 3.3 Reliability machinery (24 min)
- **Cumulative ACK semantics:** ack=N means "all bytes < N arrived; send N onward".
- **RTT estimation (simplified):** SampleRTT per RTT-measured segment; EWMA:
  EstimatedRTT = (1−α)·EstimatedRTT + α·SampleRTT (α=0.125); DeviationRTT tracked;
  **RTO = EstimatedRTT + 4·DeviationRTT** (teach the *shape*: RTO ≈ smoothed RTT +
  safety margin; exact constants per RFC 9293).
- **Retransmission triggers (the two big ones):**
  1. **Timeout:** RTO expires with no progress → resend the oldest unacknowledged
     segment; RTO backs off (doubling) under repeated loss.
  2. **Fast retransmit:** **3 duplicate ACKs** (receiver keeps sending cumulative
     ack for the gap) → resend *that* segment *without waiting for the timeout* —
     the classic capture signature (Wireshark labels it).
- **Receiver's role:** cache out-of-order segments; send duplicate ACKs while a gap
  exists; deliver in-order to the app (the "perfect stream" illusion).
- **What the students will see in GA-18:** SYN, SYN-ACK, ACK; data segments with
  increasing seq; a lost segment; 3 dup-ACKs; fast retransmit; the gap filling.
- The 3-second-unplug from the hook: segments timed out, retransmitted after RTO
  backoff, stream resumed — students now know every step of that story.

### Reference diagram — TCP three-way handshake

```text
client                                    server
   │──── SYN, seq=x ────────────────────────────→│
   │←─── SYN+ACK, seq=y, ack=x+1 ────────────────│
   │──── ACK, ack=y+1 ──────────────────────────→│
      (data may ride on segment 3)
```

## 4. Important definitions
Segment · Byte stream · ISN · Cumulative acknowledgment · Dup ACK · Fast retransmit ·
RTO (EstimatedRTT + 4·DevRTT) · Backoff · MSS · Receive/send buffer · Window (preview)
· FIN/half-close · RST · TIME-WAIT · Half-open connection · State machine (highlight).

## 5. Real-world examples
- **"Connection refused" vs timeout:** refused = RST (host alive, port closed);
  timeout = silence (host down/filtered) — the first diagnostic fork students should
  internalize for troubleshooting (L29 reuses it).
- **Gaming proxies and "TCP is laggy"**: retransmission delays *everything* after a
  loss (head-of-line blocking) — why L17's game designer asked about UDP.
- **TIME-WAIT exhaustion on busy web servers:** thousands of sockets lingering 2×MSL
  — a real capacity-planning artifact of a *correct* protocol decision.

## 6. Mathematical/technical example
Seq/ack arithmetic (board drill): client sends seq=100, 100 bytes → server acks 200.
Server sends seq=1000, 50 bytes → client acks 1050. Client sends 200→350, 300→450:
loss at 300 → server dup-acks 300 (×3) → fast retransmit of 300. Students fill a
10-row table like this on the worksheet — the mechanical heart of the lecture.
RTO numeric: SampleRTTs 100/120/90/110 ms → EstimatedRTT ≈ (weighted) ~105 ms,
Deviation ≈ 10 → RTO ≈ 145 ms; loss doubles it to ~290 — why one loss "feels like"
a stall on interactive apps.

## 7. GA-18: trace dissection (20 min)
Provided trace (handshake + 8 data segments with one loss + fast retransmit): students
annotate seq/ack values, mark the loss, count dup-ACKs, name the recovery mechanism,
and compute the recovered stream position. Wireshark's *Statistics → Flow Graph* is
the reveal. Answer key: instructor copy only.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "seq numbers count segments" | They count **bytes**; segment size varies |
| "The 3-way handshake negotiates bandwidth" | It syncs ISNs + options; capacity is learned by congestion control (L19) |
| "ACK means the app received it" | Kernel received it into a buffer; app drains separately |
| "RST is an error" | It's a legitimate abort; *diagnostically* an error sign, mechanically normal |
| "Retransmissions always wait for the timeout" | Fast retransmit via 3 dup-ACKs is the common fast path |
| "TCP connections are maintained by routers" | Pure endpoint state; the network just forwards packets (L03's point, now proven) |

## 9. Suggested practical demonstration
Live: `curl` a VM-hosted file while capturing; unplug the "link" (down a veth) for
3 s mid-transfer; show Wireshark marking retransmission + the transfer completing.
Then `ss -tn state time-wait` after a few curls to make TIME-WAIT visible. ⚠
Pre-script the veth up/down; practice the timing once.

## 10. Classroom activities
- **Human handshake:** 3 volunteers run SYN/SYN-ACK/ACK with number cards; then a
  4th student "drops" a packet — class predicts the dup-ACK dance before the trace
  confirms.
- **State-machine spotlight:** given 6 `ss` output lines, students name the state and
  what happened (ESTABLISHED/TIME-WAIT/CLOSE-WAIT/SYN-SENT...).

## 11. Problem-solving questions
1. Client seq=5000 sends 400 B. Server's ACK number? ________
2. Two-way: why does the handshake need a third packet?
3. Receiver gets seq 300–400 then 200–300 (was lost earlier). What does it send?
4. What's the difference between a FIN and an RST — and which one does "connection
   refused" use?
5. EstimatedRTT 105 ms, Dev 10 ms. RTO? After one RTO expiry (backoff)? ________

## 12. Formative assessment (with answers)
- MCQ: ack=N acknowledges → **all bytes < N**.
- MCQ: Fast retransmit is triggered by → **3 duplicate ACKs**.
- MCQ: MSS on Ethernet (IPv4) → **1460**.
- Short: why does TIME-WAIT exist? → old duplicate segments must expire before the
  4-tuple is reused.

## 13. Exit ticket
1. Sequence numbers count ________, not segments.
2. ack=1050 means the receiver expects byte ________ next.
3. 3 duplicate ACKs trigger ________ retransmission.

## 14. Anticipated difficulties
- Seq/ack arithmetic direction confusion (whose seq? whose ack?): the number-card
  drill + the 10-row table fix it; don't rush.
- Students conflate *flow control* (receiver window) with *congestion control*
  (network's) — define the boundary precisely; L19 owns the split.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify the unplug demo (veth down/up) and capture; pre-build GA-18 trace
- [ ] Prepare seq/ack drill table; state-machine `ss` outputs
- [ ] Print GA-18 worksheets; instructor answer key kept separate
- [ ] Board pre-write: segment field table; handshake diagram; RTO formula

## 16. Timing fallbacks
Drop the state-machine spotlight; GA-18 and the arithmetic table are protected (both
feed the reliable-transport project and the final exam).

## 17. References
- KR §3.5.1–3.5.4; RFC 9293 (TCP; supersedes RFC 793 — cite the current one).
- Wireshark docs (TCP analysis flags, Flow Graph); `ss`/`netstat` man pages.
- LAB-10/11 project brief (for the ladder preview).
- ⚠ VERIFY editions/sections this semester.
