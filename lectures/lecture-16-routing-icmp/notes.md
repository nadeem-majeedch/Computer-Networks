# Lecture 16 — Instructor Teaching Notes
## Routing Fundamentals & ICMP (120 min, incl. midterm)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO3/CLO4 primary; CLO6 supporting |
| Textbook anchor | KR §4.3, §5.1–5.2; PD §3.3.2 |

---

## 1. Objectives hook
Board (after midterm, during LAB-07 briefing): **"Every router asks one question per
packet: 'where next?' Today: what the table looks like, how the answer is picked, and
how routers learn the answers at all."**

## 2. Minute plan (assessment-led structure)

| Minutes | Segment | What happens |
|---|---|---|
| 0–5 | Seating/admin | Midterm papers out; integrity statement |
| 5–90 | **MIDTERM** | 90 min, Modules 1–3 (format per assessment-strategy §3.4) |
| 90–95 | Break | Papers collected; breather |
| 95–108 | Concept (compact) | Forwarding vs routing; the table; longest-prefix match |
| 108–115 | LAB-07 briefing | 3-router topology; static-route tasks |
| 115–120 | ICMP/traceroute teaser | TTL mechanic in 5 minutes (LAB-07 dissects fully) |

Deliberate deviation from the standard pattern: assessment consumes the majority.
Concepts continue next session (L17 recap covers DV/LS comparison at start if needed —
notes below provide it).

## 3. Concept walkthrough (compact, 13 min + briefing)

### 3.1 Forwarding vs routing (4 min)
- **Forwarding:** move a packet from input to output port (per-packet, data plane).
- **Routing:** build the table that guides forwarding (control plane, distributed).
- The router's one question per packet: longest-prefix match on destination.

### 3.2 The forwarding table & LPM (9 min, worked)
Table (board):

| Prefix | Next hop |
|---|---|
| 10.0.0.0/8 | R-A |
| 10.1.0.0/16 | R-B |
| 10.1.2.0/24 | R-C |
| 0.0.0.0/0 | R-default |

Destination 10.1.2.77 matches /8, /16, /24 → **/24 wins (longest prefix)**. 10.9.9.9
→ /8 only. 192.168.5.1 → default route. Rules: most-specific wins; default = last
resort; directly connected networks always beat routes.
- Tie to CS-02: their addressing plan *is* the input to tables like this.

### 3.3 How routers learn (LAB-07 briefing context, 5 min — full DV/LS at L17 recap)
- **Static:** humans write routes (LAB-07's task) — precise, no overhead, no
  adaptation.
- **Dynamic:** routers speak to routers. Two families (concept only today):
  - **Distance-vector** ("rumor"): tell neighbors your *whole* view as distances
    (RIP, hop counts; count-to-infinity problem — mention, L17's recap works an
    example).
  - **Link-state** ("map"): flood link states, each router computes shortest paths
    (OSPF — RFC 2328).
- IGP vs EGP boundary (one line): inside an AS vs between ASes (BGP — enrichment).

### 3.4 ICMP + traceroute (5 min teaser; LAB-07 dissects)
- ICMP = IP's control companion: Echo (ping), Destination Unreachable (with *codes*
  that diagnose: host/network/port), Time Exceeded (TTL=0).
- **Traceroute mechanism (already met at L04, now explained):** send with TTL=1 →
  first router drops, returns Time Exceeded with *its* source = hop 1; TTL=2 → hop 2;
  … final destination answers with Echo Reply (or unreachable port for UDP variants).
  Caveats recap: no reply ≠ broken (rate limiting/filtered), asymmetric returns.

### Reference diagram — Longest-prefix-match decision

```text
dst 10.4.9.7 vs table:
 ┌───────────────┬───────────────┬───────────────────┐
 │ 10.0.0.0/8    │ via 10.1.1.1  │ matches (8 bits)  │
 │ 10.4.8.0/22   │ via 10.1.1.9  │ matches (22 bits) │ ← WINS
 │ 0.0.0.0/0     │ via 10.1.1.254│ default           │
 └───────────────┴───────────────┴───────────────────┘
```

## 4. Important definitions
Forwarding vs routing · Control/data plane · Forwarding table · Longest-prefix match ·
Default route · Static route · Distance-vector · Link-state · IGP/EGP ·
ICMP (echo, unreachable, time exceeded) · TTL · Traceroute.

## 5. Real-world examples
- **"Why is my cloud VM unreachable from on-prem?"** — overwhelmingly a missing
  return route or a wrong next hop: the table is two-sided (ask both directions).
- **Route leak/blackhole headlines:** one AS's wrong announcement reroutes real
  traffic (BGP is enrichment, but the *class* of failure comes from today's table
  model — name it so it's not magic).

## 6. Mathematical/technical example
LPM drill set (board, 90 seconds each): table above; destinations 10.1.2.3 / 10.1.9.9 /
10.200.1.1 / 172.16.0.1 / 10.1.2.255 (careful: broadcast within connected /24 —
directly-connected handling). Students answer; errors localize the misunderstanding
immediately.

## 7. LAB-07 briefing (7 min)
Topology: R1—R2—R3 (VMs), plus a client network behind R1 and a "server" net behind
R3. Tasks: enable forwarding, add static routes so all nets reach each other, verify
with `ip route get`, capture a Time Exceeded to *prove* the TTL mechanism, run
traceroute across the topology and annotate every hop against the topology diagram.
Simulator fallback per lab-strategy §2 if kernel networking is insufficient. ⚠ Verify
VM image `ip_forward` + capture workflow; keep the reference answer config for
instructor only.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Routing = forwarding" | Table-building vs table-using; different planes |
| "The most specific route always exists" | Default route exists precisely because it doesn't |
| "Static routing is 'wrong' and dynamic is 'right'" | Static is correct at small scale/edges; dynamic for scale/adaptation — CLO6 evaluation, not religion |
| "A dropped packet means the router is broken" | TTL expiry and policy drops are normal ICMP behaviors |
| "Traceroute shows the forward path only, guaranteed" | Replies come back the *return* path; asymmetric by default |

## 9. Suggested practical demonstration
Post-midterm, during briefing: `ip route get 10.1.2.77` showing the kernel's actual
decision; one TTL=1 packet capture returning Time Exceeded. 2 minutes — the proof
students will reproduce in LAB-07.

## 10. Classroom activities
- **LPM speed round** (§6) — doubles as midterm decompression.
- **"Whose job?"** quick sort: incidents (can't reach host / slow path / wrong DNS /
  no route) → routing problem or not? (DNS one is the trap — L21 revisits.)

## 11. Problem-solving questions (LPM drill + these)
1. Table in §6: which route wins for 10.1.2.77, and why?
2. R1 can reach R2's interfaces but not the net behind R3. What's missing? (Route
   back / onward route.)
3. Why does the default route matter for every end host? (Their tables are tiny.)
4. traceroute shows `* * *` at hop 3 but hop 4 answers. Interpret.
5. What does a Destination Unreachable (host) vs (port) tell you differently?

## 12. Formative assessment (with answers)
- MCQ: Packet to 10.1.9.9 with table in §6 → **10.0.0.0/8 via R-A**.
- MCQ: Traceroute relies on → **ICMP Time Exceeded at TTL expiry**.
- Short: static vs dynamic routing — one advantage each. → static: predictable/no
  protocol overhead; dynamic: adapts to changes/failures.

## 13. Exit ticket
1. LPM rule in one line: ________
2. Traceroute's two packet types: ________ and ________
3. Control plane builds the ________; data plane uses it per ________.

## 14. Anticipated difficulties
- Midterm fatigue: keep post-exam segment hands-on and short; LAB-07's
  annotation task fits.
- LPM vs connected routes (10.1.2.255 case) trips strong students — good midterm
  follow-up question material.

## 15. Instructor preparation checklist
- [ ] ⚠ Midterm printed/portal ready; seating plan; spare papers
- [ ] LAB-07 handouts; 3-VM topology images verified
- [ ] Reference answer config (instructor-only); LPM drill set prepared
- [ ] CS-02 collection point ready (due today)

## 16. Timing fallbacks
If the midterm runs long, cut the ICMP teaser entirely (LAB-07 handout carries it);
never cut the LAB-07 briefing — topology confusion wastes lab time later.

## 17. References
- KR §4.3, §5.1–5.2; PD §3.3.2; RFC 792 (ICMP).
- RFC 2328 (OSPF — cited for link-state); LAB-07 handout.
- Midterm format: [assessment-strategy.md](../../docs/assessment-strategy.md) §3.4.
- ⚠ VERIFY editions/sections; exam moderation per assessment strategy §4.
