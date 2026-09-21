# PB-035 — Half-Open Doors (L18, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L18 — TCP Essentials: Connections & Reliable Delivery |
| CLOs | CLO2 (handshake semantics), CLO6 (read capture evidence) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual (packet level) · Topic: TCP/UDP behavior |
| Evidence policy | Synthetic capture summary, labeled; handshake/queue semantics per TCP standard |

---

## Student version

### Scenario
The portal server slows at 14:00 daily. A student captures the first seconds of the
slowdown and of a normal period:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative values):**

```
Normal period (60 s):  ~220 SYNs; ~218 SYN-ACKs; ~218 ACKs; 2 SYNs unanswered (loss)
Slowdown (60 s):       ~9,800 SYNs from 610 source IPs; ~1,900 SYN-ACKs sent;
                       ~30 ACKs; SYN-ACK retransmissions climbing (2nd, 3rd try)
Server logs:           listen queue "SYN-RCVD" count saturating; legit users see
                       connection timeouts
SYN sources:           many show spoofed/unroutable-looking addresses (no replies
                       expected — capture shows zero responses to SYN-ACKs from those)
```

### Problem statement
Explain the normal three-way handshake packet-by-packet, then explain how the observed
pattern exhausts the server's half-open connection state — including why retransmitted
SYN-ACKs make it worse.

### Evidence pack
The labeled synthetic capture. Facts: SYN-ACKs vastly outnumber ACKs; sources
unresponsive; queue saturation logged.

### Constraints
- Name the state each packet moves the connection through (SYN-SENT/SYN-RCVD/
  ESTABLISHED).
- Do not propose DDoS countermeasures beyond naming the *mechanism* (this is a
  diagnosis case).

### Student questions
1. Write the three-way handshake as packet/state pairs for a healthy connection.
2. In the slowdown capture, what fraction of offered handshakes completes? Show the
   arithmetic.
3. Why do retransmitted SYN-ACKs *extend* the damage? (What state do they preserve?)
4. Why does spoofing the source IP make this attack especially effective against the
   half-open queue?

### Expected learning outcomes
- Narrate the handshake with connection states.
- Explain the half-open (SYN-RCVD) queue as a finite resource.
- Connect spoofing to unanswerable handshakes and queue exhaustion.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Each packet has a job: propose, accept, confirm. Which states does the *server*
   occupy between packets?"
2. "The server keeps half-built connections on a shelf. Every unanswered SYN-ACK sits
   there — and gets *re-shelved* on each retransmission."

### Solution
1. Healthy: client SYN → client SYN-SENT / server SYN-RCVD; server SYN-ACK → server
   still SYN-RCVD / client ESTABLISHED; client ACK → server ESTABLISHED. Three packets,
   two state machines.
2. Slowdown: 30 ACKs / 9,800 SYNs ≈ **0.3%** completion (vs ~99.9% normal:
   218/220). The queue fills with SYN-RCVD entries that never complete.
3. On SYN-ACK timeout the server retransmits (typically several times with backoff ⚠
   defaults per implementation), keeping each half-open entry alive for tens of
   seconds to minutes. Every retransmission *extends* the entry's lifetime, so the
   queue stays saturated even if new SYN arrivals merely match the drain rate.
4. A spoofed source never receives the SYN-ACK, so the client ACK never comes; the
   entry lives until retransmission cycles exhaust. Spoofing turns "slow clients" into
   "no clients" — the handshake's state memory becomes the attack surface. (Mechanism
   only; mitigations like SYN cookies are out of scope here but worth one sentence:
   they exist precisely because state-before-ACK is expensive.)

### Reasoning process
Facts: completion fraction collapse, unresponsive sources, queue saturation,
retransmissions. Model: handshake state machine + finite half-open table + timeout-
based retention. Attack mechanism: uncompletable handshakes × retention = exhaustion.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "The server is out of bandwidth" | ~9,800 SYNs/min is trivial volume; the scarcity is *connection state*, not bits |
| "The clients are buggy" | The 0.3% completion and unresponsive sources indicate deliberate/abusive non-completion — but mechanically, any unresponsive source (even accidental) does the same |
| "Close ports" | The service must stay open; the fix class is state-management, not access removal (out of scope here) |
| Ignore retransmissions | They are the persistence mechanism — without them the queue would drain in seconds |

### Extension question
SYN cookies sidestep the queue by encoding connection state into the SYN-ACK's
sequence number. Which handshake property makes that possible, and what does the
server *not* store while cookies are active? (Sequence-number arithmetic lets the
server validate the incoming ACK and reconstruct the state deterministically; it
stores nothing per half-open connection — the state lives in the *client's* ACK. Some
TCP options may be lost in cookie mode ⚠ implementation detail.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Handshake with states; 0.3% arithmetic; retransmission-retention mechanism; spoofing→queue link precise |
| 3 Proficient | Handshake + queue exhaustion; retransmission role partial |
| 2 Developing | "Too many connections" without state mechanics |
| 1 Beginning | Restarts the server |

### References
- PD §3.5 (connection-oriented transport), §3.5.6/§3.5.7 (connection management) ⚠ verify
- Kurose & Ross §3.5.2 (TCP connection management); RFC 9293 §3.10 (states)
