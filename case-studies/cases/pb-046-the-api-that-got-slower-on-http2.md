# PB-046 — The API That Got Slower on HTTP/2 (L23, Advanced)

| Field | Value |
|---|---|
| Difficulty | **Advanced** |
| Lecture(s) | L23 — Core Application Protocols: HTTP/1.1 → HTTP/3, SMTP & SSH |
| CLOs | CLO6 (protocol trade-off evaluation), CLO2 (transport/application interaction) |
| In-class slot | Extended activity; 25 min, groups of 3 |
| Case type | Diagnostic + trade-off · Topic: Application protocols / performance |
| Evidence policy | Synthetic measurements, labeled; H2/H3 framing per published specs (RFC 9113/9114 ⚠); internally consistent |

---

## Student version

### Scenario
The dashboards team migrated the analytics API gateway from HTTP/1.1 to HTTP/2 and
expected wins. Aggregate throughput rose slightly — but the *interactive* endpoint
(`GET /live-scores`) became erratic: p95 latency rose from 120 ms to 800+ ms during
busy periods, exactly when heavy `POST /export` jobs run.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
Gateway:        HTTP/2 over TCP, one connection per client; flow-control window
                64 KB per stream (default-ish), connection window 128 KB
Busy-period trace (one client, one connection):
  t0      POST /export starts (streams a 200 MB CSV; response consumes the
          connection window as fast as ACKs allow)
  t0..t8s GET /live-scores issued on the SAME connection every 250 ms
  observed live-scores p50: 130 ms; p95: 840 ms; p99: 1.9 s
  (during t0..t8s only)
Calm-period trace: live-scores p95: 120 ms (unchanged from H1.1 baseline)
Retransmissions: ~0 (link is clean)
H1.1 comparison (pre-migration, same load): export used a separate connection;
  live-scores unaffected (p95 125 ms)
```

### Problem statement
Explain the mechanism by which one large response degrades a *different* stream on the
same connection under HTTP/2 (name the blocking type and where exactly it bites:
which layer's window, which queue). Then evaluate three remedies and pick one.

### Evidence pack
The labeled synthetic traces. Facts: clean link (no loss); correlation with export
jobs; same-connection-only effect; H1.1 baseline fine because connections were
separate.

### Constraints
- The mechanism must explain why *no retransmissions* still produces 1.9 s p99.
- Remedies: (a) per-path connection isolation (undo the multiplexing for hot paths),
  (b) stream priority/window tuning, (c) HTTP/3 (QUIC). One trade-off each; pick.

### Student questions
1. Where does the live-scores response *wait* during an export? Walk one
   live-scores request-response through the shared pipe and name the stall point.
2. Why doesn't H2 stream multiplexing prevent this? (What does multiplexing share,
   and what does it not share?)
3. The evidence shows "no retransmissions" yet 1.9 s p99 — why is that consistent
   with the mechanism (and what *would* retransmission-based blocking look like
   instead)?
4. Remedies: one trade-off each; which do you deploy first and why?

### Expected learning outcomes
- Distinguish H2 application-level multiplexing from TCP-level ordering (HOL at
  TCP).
- Explain flow-control windows and shared-pipe queueing effects.
- Evaluate H2/H3 remedies with deployment-first reasoning.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Both responses share one ordered byte stream at TCP. The export's bytes and the
   scores' bytes are interleaved at HTTP/2 — but what does TCP promise about
   ordering?"
2. "Flow control says each stream *may* send; the socket has one send buffer. Who
   queues first, and who is stuck behind whom?"

### Solution
1. The live-scores response (~2 KB) is generated quickly but enters the connection's
   single TCP send queue behind megabytes of export CSV that the receiver's H2
   connection window is happily accepting. TCP delivers bytes *in order*; the scores
   bytes sit behind export bytes in the socket buffer ⇒ delivery waits for the
   export to drain. The stall point: **the shared TCP send path** (application-level
   multiplexing happens; transport-level ordering does not).
2. Multiplexing shares: one connection, one congestion window, one ordered byte
   stream, one flow-control budget at the connection level. It does *not* give each
   stream its own transport queue — H2 removes HTTP/1.1's *application-layer* HOL
   (no more waiting for a whole request/response) but inherits TCP's *transport-
   layer* HOL: any retransmission or big-backlog stalls all streams' bytes equally.
3. No retransmissions ⇒ no *loss-triggered* HOL (where one lost segment stalls every
   stream until re-ACKed). This is *backlog HOL*: the export's sheer byte volume
   occupies the ordered pipe; scores' bytes are correctly delivered, just late. The
   distinction matters for the remedy: loss-HOL would invite H3; backlog-HOL
   responds to scheduling/window/connection choices.
4. Remedies: (a) **connection isolation per hot path** (re-create the H1.1 behavior
   for /live-scores: separate connection or separate gateway instance): immediate,
   low-risk, concedes H2's connection efficiency for that path — trade-off: more
   connections/handshakes, loses shared congestion context. (b) **window/priority
   tuning**: shrink the connection flow-control window or cap export stream rate
   (chunk + pacing) so the pipe drains between scores' turns — trade-off: throttles
   export throughput; priority hints don't preempt bytes already in the socket
   buffer ⚠ (they influence what the *sender* emits next — partial control only).
   (c) **HTTP/3/QUIC**: per-stream flow control + independent delivery — solves both
   backlog-HOL and loss-HOL properly; trade-off: infrastructure/ops maturity, UDP
   path traversal quirks ⚠. Deploy **(a) first** (hours of work, exact target,
   reversible), evaluate (c) as the strategic fix once the path is stable.

### Reasoning process
Facts: same-connection-only degradation, clean link, H1.1-baseline fine, correlation
with exports. Model: H2 multiplexes at application layer; TCP orders at transport
layer; backlog HOL from byte-volume sharing, not loss. Remedy selection: target the
stall point directly (isolation) before infra change (H3).

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "H2 is broken / roll back to H1.1" | H1.1 only looked fine because it *accidentally* isolated paths via separate connections; understanding the mechanism enables (a) surgically |
| "Enable stream priorities" | Priorities shape what the sender emits next; they cannot reorder bytes already queued in TCP — the scores' bytes were already behind megabytes ⚠ |
| "It's the 64 KB stream window — raise it" | Raising windows lets the export drain *faster into the same pipe*; the scores wait behind a taller flood |
| "Blame the client" | Same client, calm period: 120 ms p95 — the variable is the shared pipe, not the endpoint |

### Extension question
A colleague proposes gRPC (HTTP/2-based) for everything "since it multiplexes". Given
this case, what question must you ask about *every* endpoint mix before agreeing?
(What shares a connection with what: mixing large-fan-out bulk streams and sub-100 ms
interactive streams on one H2 connection reintroduces backlog HOL; per-service
connection partitioning or H3 changes the answer. The general lesson: multiplexing is
a sharing decision — ask what you're sharing with whom.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Stall point named precisely; multiplexing vs ordering distinction; backlog-vs-loss HOL fork; remedy trade-offs + deployment order |
| 3 Proficient | Mechanism right; HOL fork or remedy nuance missing |
| 2 Developing | "H2 head-of-line blocking" as a slogan without the layer analysis |
| 1 Beginning | Rolls back the migration |

### References
- RFC 9113 (HTTP/2: streams, flow control) ⚠ verify sections; RFC 9114 (HTTP/3) ⚠
- Kurose & Ross §2.2 (HTTP evolution context)
