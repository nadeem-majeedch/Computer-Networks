# Weekly Quiz — Week 08 (L15, L16) — midterm week, keep light

| Field | Value |
|---|---|
| Coverage | L15 — IPv6 · L16 — Routing fundamentals & ICMP |
| Mode | Formative, ~8 min (midterm week — deliberately short), individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO3|L15]** Abbreviate 2001:0db8:0000:0000:0000:ff00:0042:8329 per RFC 5952
rules (one `::` at the leftmost run, leading zeros dropped).

**Q2 [I|CLO3|L15]** What is an fe80::/10 link-local address for, and can it be routed?

**Q3 [I|CLO4|L16]** Routing table on R: `10.0.0.0/8 → R1` · `10.1.0.0/16 → R2` ·
`10.1.5.0/24 → local LAN`. Which next hop does R choose for 10.1.5.9, and which rule
decides?

**Q4 [I|CLO4|L16]** In `traceroute`, what causes the intermediate replies, and which
ICMP type/message is it?

**Q5 [B|CLO4|L16]** What two ICMP messages implement ping, and what single number does
ping primarily report?

**Q6 [I|CLO6|L16]** Packets to one destination always die after exactly 3 hops with
"ICMP time exceeded". Distinguish a routing loop from a too-small TTL on the *sending
host*, and name the evidence for each.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** `2001:db8::ff00:42:8329` [MC]. [B·CLO3]

**Q2.** Link-local addresses work only on a single link (auto-configured, no DHCP
needed); routers must not forward them between links (not globally routable). [I·CLO3]

**Q3.** Local LAN — **longest-prefix match** wins over shorter prefixes regardless of
routing-protocol metric. [I·CLO4]

**Q4.** Each intermediate router decrements TTL; at 0 it drops the packet and returns
**ICMP Time Exceeded (Type 11, code 0 — TTL exceeded in transit)**. Traceroute infers
hop identity from that reply's source. [I·CLO4]

**Q5.** Echo Request (Type 8) and Echo Reply (Type 0); ping primarily reports RTT
(plus loss, from missing replies). [B·CLO4]

**Q6.** Loop: TTL dies at increasing *or* patterned hop counts when probed with
different TTLs from the same source, and TTL at the *first* failing router is high —
evidence: traceroute shows the path cycling between the same two/three routers. Too-small
TTL on the sender: failure is at a consistent early hop *only for this sender*, while
other sources reach the destination — evidence: compare from a second source, or raise
the initial TTL. The distinguishing evidence is comparative, not the single trace. [I·CLO6]
