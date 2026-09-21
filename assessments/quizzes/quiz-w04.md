# Weekly Quiz — Week 04 (L07, L08)

| Field | Value |
|---|---|
| Coverage | L07 — MAC protocols & wired LANs: Ethernet · L08 — Switching & LAN design |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | **Graded-quiz candidate window** (strategy §2; see assessments/README.md §5 reconciliation note) |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO2|L07]** Why did CSMA/CD become obsolete in modern switched Ethernet? Refer
to duplex mode and physical design in your answer.

**Q2 [I|CLO4|L07]** Name four fields of the Ethernet frame proper (excluding preamble
and SFD) and state which field the receiver uses to decide whether to accept the frame.

**Q3 [I|CLO2|L08]** A switch receives a frame for destination MAC *M* that is **not** in
its forwarding database. What does it do, and how does *M*'s eventual reply change the
switch's table?

**Q4 [I|CLO6|L08]** A single switch connects four PCs, and one router uplink. How many
collision domains and how many broadcast domains exist? Justify each count.

**Q5 [I|CLO4|L07]** Ethernet's minimum frame size is 64 bytes (512 bits). How long does
such a frame occupy a 1 Gb/s link (serialization time)? Show working.

**Q6 [I|CLO6|L08]** PC-A and PC-B sit on the same switch, same VLAN, and A cannot reach
B. You capture on A's port: A's ARP request is visible, B's ARP reply is **not**. From
switch behavior, give the two most plausible causes and one command/check for each.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Modern links are full-duplex over separate twisted pairs/fiber paths through a
switch port — stations transmit and receive simultaneously with no shared medium, so
collisions cannot occur and carrier-sense/collision-detection logic has no role. [B·CLO2]

**Q2.** Destination MAC, source MAC, EtherType/Length, payload, FCS (any four). The
**FCS** (CRC-32) is checked first — a mismatched frame is discarded before learning
(forwarding happens only for good frames; this nuance accepted either way). [I·CLO4]

**Q3.** Unknown unicast → **flood** out every port in the VLAN except the ingress port.
When M replies, the switch learns M ↔ ingress port from the **source** MAC of the reply
and forwards subsequent frames there directly. [I·CLO2]

**Q4.** Collision domains: four — each switched port is its own full-duplex collision
domain (the router uplink is the fourth port). Broadcast domains: one — a switch floods
broadcasts within the VLAN; only a router (or VLAN boundary/L3 device) separates
broadcast domains. [I·CLO6]

**Q5.** 512 bits / 10⁹ b/s = **512 ns** [MC]. [I·CLO4]

**Q6.** (i) B's port/link is down or B never replied — check switch FDB for B's MAC
(aging/absence) or B's interface state (`ip link`). (ii) Filtering asymmetry: reply
blocked on B's side (e.g., ACL or B's reply never generated) — capture on B's port to
confirm whether B sent a reply. Full credit requires capturing logic "request seen on A's
port; verify on B's port." [I·CLO6]
