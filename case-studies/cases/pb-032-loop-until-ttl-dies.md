# PB-032 — Ping-Pong Between Two Routers (L16, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L16 — Routing Fundamentals & ICMP |
| CLOs | CLO2 (TTL/loop semantics), CLO6 (diagnose from path evidence) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Diagnostic · Topic: Routing faults |
| Evidence policy | Synthetic traceroutes/configs, labeled; TTL semantics per IPv4 spec |

---

## Student version

### Scenario
After a "quick fix" for a dead link, traffic from Branch to the micro-datacenter
(10.20.70.0/26) looped until someone reverted the change. You get the before/mid/after
traceroutes and the change note.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
Change note: "R-branch dead link to R-hq; added static: 10.20.0.0/16 via 192.0.2.9
              (micro-datacenter link) as a temporary workaround."

MID-INCIDENT traceroute from branch client to 10.20.70.70:
  1  10.100.5.1 (R-branch)
  2  192.0.2.9  (R-mdc)
  3  10.100.5.1 (R-branch)      ← same IP as hop 1
  4  192.0.2.9  (R-mdc)
  5  10.100.5.1 (R-branch)
  6  192.0.2.9  (R-mdc)
  7  * * *
  8  * * *
  ...
AFTER revert: traceroute normal (2 hops to destination, via R-mdc)
Ping during incident: "Time to live exceeded in transit" (from one of the routers)
```

### Problem statement
Explain the loop mechanically (what each router believed), explain how TTL converted an
infinite loop into a finite failure, and evaluate the change practice that allowed it.

### Evidence pack
The labeled synthetic traceroute/config note. Facts: alternating next hops; TTL
exceeded messages; revert fixed it. You may assume: R-mdc had a route to
10.20.70.0/26 → its own LAN; R-branch's new static covered *all* of 10.20.0.0/16.

### Constraints
- Explain why R-mdc sent the packet *back* to R-branch (what its table must have
  contained — one labeled inference).
- Connect TTL decrement to the observed hop count where stars begin (state the
  default 64 assumption ⚠ varies).

### Student questions
1. Walk one packet's journey through three loop iterations. What did R-branch and
   R-mdc each believe about 10.20.70.70?
2. Why did the packet finally die, and why at hop ~8 in the traceroute rather than
   continuing forever? (TTL arithmetic.)
3. The ICMP "TTL exceeded" message: who generates it, and why is it *useful* (not just
   an error)?
4. Evaluate the change: what two safety steps were skipped, and what minimal change
   would have delivered the same workaround safely?

### Expected learning outcomes
- Reconstruct forwarding-state beliefs from path evidence.
- Explain TTL as the loop-breaker and its arithmetic.
- Critique change practice with concrete, minimal safeguards.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "R-branch sent the packet to R-mdc. For R-mdc to send it *back*, what must its table
   have said about 10.20.70.70 — and is that plausible given the incident context?"
2. "Every router decrements TTL by one. 64 vs the observed hop count — where does 64
   fit the trace?"

### Solution
1. R-branch: "10.20.70.70 ⊂ 10.20.0.0/16 → via 192.0.2.9 (R-mdc)" (the new static).
   R-mdc: received a packet for 10.20.70.70 — a subnet *it hosts* — but sent it back
   to R-branch. Inference (labeled): R-mdc's own route to 10.20.70.0/26 was broken/
   withdrawn (its uplink/LAN interface was down — plausibly *the same* dead link the
   workaround targeted, or the LAN SVI failed), so R-mdc's table matched only its
   default → back toward R-branch. Ping-pong.
2. Each hop decrements TTL; at TTL=0 the router drops and emits ICMP Time Exceeded.
   With the common initial TTL 64 ⚠ (per-OS default), a data packet dies after 64 loop
   hops. The trace's stars from hop ~7 are honest to explain as two stacked mechanisms,
   both flagged ⚠: each looping *probe* burns three hops per line (traceroute counts
   the same cycle thrice), quickly reaching routers' ICMP rate-limits — probes then
   draw no reply, printing `* * *`. Meanwhile the underlying data path kept cycling
   until TTL death. Teaching point: TTL bounds the loop; the alternating hops prove it.
3. The router that decrements TTL to zero generates ICMP Time Exceeded *back to the
   source*. Useful: (a) it's how traceroute maps paths (each hop's reply reveals the
   router); (b) it tells the sender the packet died *and where* — the error message
   quotes the original datagram, which is how admins confirm loop membership (both
   routers' ICMP quotes the same packet).
4. Skipped: (a) reachability/dependency check — the workaround assumed R-mdc could
   deliver 10.20.70.0/26, which was false at the time; (b) scoping — a /16 static
   covered far more than the /26 target, maximizing blast radius. Minimal safe change:
   static for **10.20.70.0/26** only, *after* verifying R-mdc's LAN route, with a
   documented revert step and a post-change traceroute from a branch client (which
   would have caught the loop in seconds).

### Reasoning process
Facts: alternating hops, TTL exceeded, revert restored service, change note scope.
Model: complementary routing beliefs → cycle; TTL bounds it; ICMP exposes it.
Diagnosis from path shape alone; change critique: dependency verification + scope +
post-change verification.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Traceroute is buggy — it repeats hops" | The repetition IS the evidence; the path really cycles |
| "Broadcast storm" | L3 loop; no broadcast involvement (unicast ping-pong) |
| "R-mdc should have known better" | Forwarding is table-driven; its table (labeled inference: dead LAN route) dictated the bounce — fault lies in unverified change assumptions |
| "Add more statics to fix" | Compounds the original sin; correct the dependency, scope the route |

### Extension question
Dynamic routing (e.g., a routing protocol with loop-avoidance) *also* produces
transient loops during convergence. What differs about those loops vs this static one,
in terms of duration and self-healing? (Protocol loops are typically transient — state
converges and the loop dissolves; a static-route loop is *permanent configuration
truth* until a human edits it. That asymmetry is why change control matters more for
statics.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Both routers' beliefs reconstructed with labeled inference; TTL arithmetic + traceroute-star honesty; change critique with minimal safe alternative |
| 3 Proficient | Loop mechanism correct; TTL/star details hand-waved |
| 2 Developing | "Routing loop" restated; no belief reconstruction |
| 1 Beginning | Reboots routers |

### References
- PD §4.2 (routing/forwarding), §4.3 (IPv4 TTL semantics) ⚠ verify sections
- Kurose & Ross §4.3.1 (IPv4 datagram: TTL), §5.2 (routing state) context
