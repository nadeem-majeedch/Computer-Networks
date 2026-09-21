# Weekly Quiz — Week 07 (L13, L14)

| Field | Value |
|---|---|
| Coverage | L13 — Subnetting & VLSM · L14 — DHCP & NAT |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | **Graded-quiz candidate window** (strategy §2; see assessments/README.md §5 reconciliation note) |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [I|CLO3|L13]** From 10.20.0.0/22 allocate: one subnet for a 60-host staff LAN and
one /30 for a router-to-router link. Give prefix, range, and waste hosts for each; state
your ordering rule.

**Q2 [B|CLO3|L13]** How many /28 subnets fit in a /24, and how many usable hosts does
each /28 hold?

**Q3 [I|CLO4|L14]** List the DHCP DORA exchange and state, with one reason, which
messages are broadcast and which are typically unicast.

**Q4 [I|CLO4|L14]** For outbound NAT at a home router: which header fields change, and
what state must the router keep so replies return to the right LAN host?

**Q5 [I|CLO6|L14]** Two staff PCs report "no network" on Monday morning. PC-1 got
169.254.x.x; PC-2 got 192.168.7.50. Give the most likely distinct cause for each and
the DHCP concept each illustrates.

**Q6 [I|CLO3|L13]** How many usable host addresses does a /22 provide, and what two
addresses are excluded?

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Order largest-first: staff LAN **10.20.0.0/26** (usable 10.20.0.1–.62; 62 hosts —
2 spare), link **10.20.0.64/30** (usable 10.20.0.65–.66; 2 wasted of 4 for network +
broadcast). Any consistent allocation order accepted if ranges don't collide and the
ordering rule is stated (e.g., "largest first to keep alignment") [MC]. [I·CLO3]

**Q2.** 16 subnets; 14 usable hosts per /28 (16 − network − broadcast) [MC]. [B·CLO3]

**Q3.** Discover → Offer → Request → Ack. Discover is broadcast (client has no address
yet); Request typically broadcast (confirms chosen server to all offerers); Offer/Ack
typically unicast from server once the client's offered identity allows it — reason:
broadcast is needed only where the client cannot yet be addressed. [I·CLO4]

**Q4.** Outbound: source IP → router's public IP, source port → a translated (NAT) port;
destination unchanged. State: the mapping (public IP:port ↔ inside IP:port, plus
protocol and timeout) so reply packets to public IP:port are rewritten back to the
inside host. [I·CLO4]

**Q5.** PC-1: no DHCP reply at all → APIPA/link-local self-address (169.254.0.0/16) —
illustrates DHCP failure (cabling/port/server down). PC-2: got an address but maybe the
**wrong scope/gateway** (192.168.7.x while staff subnet is different) — illustrates
scope/configuration mismatch; verify router/gateway config rather than cabling. [I·CLO6]

**Q6.** 1024 addresses − network − broadcast = **1022 usable** [MC]; excludes the
all-zeros host (network) and all-ones host (broadcast) of the /22. [I·CLO3]
