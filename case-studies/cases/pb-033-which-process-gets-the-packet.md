# PB-033 — Which Process Gets the Packet? (L17, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L17 — UDP & the Transport Layer's Job |
| CLOs | CLO2 (ports & demultiplexing), CLO4 (reason about socket state) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Conceptual trace · Topic: Network programming (transport) |
| Evidence policy | Synthetic socket/flow table, labeled; demux rule per UDP semantics |

---

## Student version

### Scenario
A student's sensor gateway runs three UDP apps on one host. A teammate insists "two
apps can't share port 5000 — the OS will complain." The traffic matrix says otherwise
— or does it?

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Host 10.20.30.9, running:
  A: telemetry collector   bound UDP 0.0.0.0:5000
  B: metrics exporter      bound UDP 0.0.0.0:5001
  C: lab probe             bound UDP 192.168.56.10:5000   (secondary IP on same NIC)
Observed flows (all arriving correctly):
  F1: 10.20.30.55:41234 → 10.20.30.9:5000
  F2: 192.168.56.20:55555 → 192.168.56.10:5000
  F3: 10.20.30.55:41234 → 10.20.30.9:5001
  F4: 10.20.30.77:41234 → 10.20.30.9:5000
```

### Problem statement
Explain the demultiplexing rule that routes F1–F4 to the right sockets, and settle the
teammate's claim precisely: when *can* two sockets share a port number on one host?

### Evidence pack
The labeled synthetic bind/flow table. Rule from lecture: UDP demux key = (dest IP,
dest port, source IP, source port) — with wildcards matched appropriately.

### Constraints
- Trace each flow to exactly one socket (A, B, or C).
- The teammate's claim must be resolved as "true/false/conditionally true" with the
  exact condition.

### Student questions
1. F1: which socket and why (state the matching rule components)?
2. F2: which socket? What distinguishes it from F1 at the demux level?
3. F3 vs F1: same 4-tuple except the port. Why do they never collide?
4. Verdict on the teammate's claim: complete the sentence "Two sockets may share the
   same port number when ______" — give the two standard cases.

### Expected learning outcomes
- Apply UDP demultiplexing (destination IP+port first, then source tuple).
- Distinguish wildcard vs specific binds on one host.
- Correct the "one port = one app" misconception with precise conditions.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The demux key isn't just the port. List every field the OS can match on."
2. "One bind is a wildcard (0.0.0.0), the other names a specific local IP. Which wins
   for F2 — and why does F1 not reach C?"

### Solution
1. F1 → **A**: dest IP 10.20.30.9, dest port 5000 matches A's wildcard bind
   (0.0.0.0:5000 matches any local IP). C's bind is *specific* to 192.168.56.10:5000 —
   F1's dest IP doesn't match it. Specific binds outrank wildcards for their address;
   non-matching addresses fall to wildcards.
2. F2 → **C**: dest IP 192.168.56.10 matches C's specific bind exactly — the OS
   prefers the more specific (fully-qualified) socket over A's wildcard even though
   both listen on 5000.
3. F3 and F1 differ in dest port (5001 vs 5000) — different demux keys, so B and A
   receive respectively; no collision despite identical source tuple
   (10.20.30.55:41234).
4. "Two sockets may share the same port number when (a) they bind *different local IP
   addresses* (e.g., A wildcard vs C specific — with the caveat that binding wildcard
   after a specific bind can fail with SO_REUSEADDR semantics differing per OS ⚠), or
   (b) they are UDP sockets with *different remote endpoints* (connected UDP sockets
   keyed by source tuple) — or on TCP, different connections (4-tuple). The bare
   claim 'can't share' is false but *conditionally* protective for untrained users."

### Reasoning process
Facts: three binds (one wildcard, two distinct ports, one specific-IP) and four flows.
Model: demux by (dst IP, dst port) then (src IP, src port); wildcard as fallback.
Classify each flow; resolve the claim by enumerating the share conditions.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Port alone decides" | The dest IP is part of the key; wildcard vs specific binds exist precisely for this |
| "F2 goes to A because A bound 5000 first" | Specific-match precedence; bind order isn't the rule (OS differences ⚠ noted for edge cases) |
| "UDP has no demux, it's fire-and-forget" | Unreliable *delivery* ≠ unaddressed; every datagram still lands in exactly one socket |

### Extension question
The team adds D, a second telemetry collector, bound 0.0.0.0:5000. What happens to F1
and F2, and what socket option (and OS caveat ⚠) is the standard remedy when multiple
processes must *share* a wildcard receive path? (F1/F2 become ambiguous → bind fails
with EADDRINUSE unless SO_REUSEPORT (Linux ⚠; SO_REUSEADDR semantics differ on other
OSes) is set; kernel then load-balances datagrams across the group.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All flows routed with rule components named; specific-vs-wildcard precedence; two share conditions with OS caveat flagged |
| 3 Proficient | Flows correct; share conditions incomplete |
| 2 Developing | Demuxes by port only; F2 misrouted |
| 1 Beginning | "Two apps one port = crash" |

### References
- PD §2.1 (multiplexing/demultiplexing), §3.3 (UDP) ⚠ verify section mapping
- Kurose & Ross §3.2 (multiplexing), §3.3 (connectionless transport)
