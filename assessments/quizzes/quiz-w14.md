# Weekly Quiz — Week 14 (L27, L28)

| Field | Value |
|---|---|
| Coverage | L27 — Cloud & virtual networking · L28 — SDN & programmable networks |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO6|L27]** Name the virtual network component in a container host that
connects container namespaces to the outside, and the address-translation step usually
required for outbound connections.

**Q2 [I|CLO6|L27]** A containerized service's large transfers stall while small ones
succeed. Using L27's most common culprit, name it and the setting to compare with the
path's minimum MTU.

**Q3 [I|CLO6|L27]** In an overlay network (e.g., VXLAN-style), what is the underlay and
what is carried over it?

**Q4 [B|CLO6|L28]** Sort into control/data/management plane: (i) operator pushes a
config template, (ii) switch forwards a frame using its table, (iii) routing protocol
recomputes paths after a link fails.

**Q5 [I|CLO6|L28]** An SDN controller programs switches with match/action rules. Give
one reachability rule (in words) for "H1 may reach H2 via switch S1," and one
policy rule for "H3 is denied to H2."

**Q6 [I|CLO6|L28]** State one operational risk introduced by centralizing control plane
decisions, and the standard engineering mitigation.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** The container host's bridge/virtual switch (e.g., docker0-style bridge +
veth pairs) connects namespaces; outbound traffic is source-NAT'd (masqueraded) to the
host's address. [B·CLO6]

**Q2.** **MTU mismatch** — an encapsulation/overlay shrinks the effective path MTU and
large packets are dropped while handshakes (small) succeed. Compare the interface MTU
(and overlay overhead) against path MTU; fix by matching MTU or enabling correct
path-MTU handling. [I·CLO6]

**Q3.** The underlay is the physical/routed IP fabric; the overlay carries tenant
*frames/packets encapsulated* inside underlay datagrams (tenant L2 segments tunneled
across the L3 network). [I·CLO6]

**Q4.** (i) management plane · (ii) data (forwarding) plane · (iii) control plane. [B·CLO6]

**Q5.** Reachability (words acceptable, e.g., match: in-port H1, dst H2 → action:
forward out S1's port toward H2). Policy: match: src H3, dst H2 → action: drop. Key
point: match+action replaces per-switch autonomous learning decisions. [I·CLO6]

**Q6.** The controller is a single point of failure/latency: its outage freezes global
reconfiguration (existing flows usually keep forwarding, but *changes* stop). Mitigation:
controller clustering/redundancy plus autonomous fallback behavior on switches — accept
either named explicitly. [I·CLO6]
