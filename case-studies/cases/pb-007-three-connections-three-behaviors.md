# PB-007 — Three Connections, Three Behaviors (L03, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L03 — Applications, Sockets & the Packet's Journey |
| CLOs | CLO1, CLO4 (interpret socket-level outcomes) |
| In-class slot | Closing consolidation; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: Network programming |
| Evidence policy | Synthetic test outcomes, labeled; each behavior maps to one standard TCP-level cause |

---

## Student version

### Scenario
A student writes a Python TCP client for the data-science cluster and tests it against
three lab endpoints from the same machine, same minute:

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
To node-a:5050 → ConnectionRefusedError, immediately
To node-b:5050 → hangs ~75 s, then TimeoutError
To node-c:5050 → connects, then ConnectionResetError after 2 s of data
```

### Problem statement
Explain what each behavior says about the packet exchange (what was sent, what came
back — or didn't), and name the most likely cause for each endpoint.

### Evidence pack
The labeled synthetic outcomes. Assume the client and all three nodes are on the same
isolated lab subnet; no firewalls between them except where stated by a behavior.

### Constraints
- Reason at the TCP level (what does *refused* mean on the wire? what does a timeout
  mean?); no guessing about code bugs beyond the socket layer.
- One most-likely cause per endpoint; alternatives must be argued, not listed.

### Student questions
1. Node-a: what packet(s) came back, and who sent them? Most likely cause?
2. Node-b: what is notably *absent* on the wire, and what two causes fit? Which is more
   likely on an isolated lab subnet, and why?
3. Node-c: the connection was *established* — so which layers are proven working before
   the reset? What does the reset most likely indicate?
4. Rank the three by "how much of the stack is proven good" and justify the order.

### Expected learning outcomes
- Distinguish refused vs timeout vs reset at the packet level.
- Infer listener state, reachability, and application behavior from connection outcomes.
- Reason about what a successful handshake proves — and what it doesn't.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "Refused is a *reply*, not silence. Who replies to a SYN for a closed port?"
2. "A reset after data is an application or kernel-level statement — the path already
   carried a full handshake plus payload."

### Solution
1. Node-a: an RST (or ICMP port-unreachable equivalent) came back **from node-a's TCP
   stack** — the host is up but nothing is listening on 5050 (or the port is closed).
   Most likely: server not started / wrong port.
2. Node-b: nothing comes back — no SYN-ACK, no RST. Two fits: host down/off (or wrong
   IP), or a firewall silently dropping (filtering). On an isolated lab subnet with no
   firewall policy, **host down / wrong address** is more likely; a dropped-datagram
   firewall is the alternative to argue explicitly.
3. Node-c: L1–L4 path proven (SYN, SYN-ACK, ACK all traveled) *and* application data
   flowed both directions for 2 s. The reset most likely came from node-c's side — the
   application crashed, closed abruptly, or actively rejected the session (e.g., a
   protocol-level error or server restart).
4. Node-a proves L1–L3 reachability + a live TCP stack (least proven: no application).
   Node-c proves the most (full handshake + data). Node-b proves the least. Order:
   **c > a > b**.

### Reasoning process
Facts: three distinct outcomes from one vantage point. Model: refused = RST reply
(listener absent); timeout = no reply (unreachable or filtered); reset-after-data =
established session torn down by the peer. Map outcome → path knowledge.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Refused = firewall blocked me" | A block produces *silence* (timeout); a refusal is an explicit reply |
| "Timeout = server busy" | Busy servers queue or refuse; a timeout means no reply at all from that address |
| "Reset = network error" | The handshake succeeded; resets come from an endpoint's stack/application |
| Treating all three as "the server is broken" | The three outcomes have different culprits and different fixes |

### Extension question
The student adds `settimeout(5)` on the socket. For node-b, what changes in observed
behavior, and what *doesn't*? (Observed: TimeoutError at 5 s instead of 75 s; unchanged:
the silence on the wire — the timer is client-side cosmetics, not diagnosis.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | All three packet-level narratives correct; Q4 ordering justified; hints of firewall-vs-down distinction in Q2 |
| 3 Proficient | Two of three causes correct; one conflation (e.g., refused vs filtered) |
| 2 Developing | Describes behaviors in app terms only ("it crashed") without packet reasoning |
| 1 Beginning | guesses; no TCP model |

### References
- PD §2.1.2, §3.3 (TCP connection management: SYN, RST semantics)
- Kurose & Ross §3.5.2 (connection establishment); RFC 9293 §3.10 (connection states)
