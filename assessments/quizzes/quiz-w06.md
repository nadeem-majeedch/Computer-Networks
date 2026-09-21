# Weekly Quiz — Week 06 (L11, L12)

| Field | Value |
|---|---|
| Coverage | L11 — Wireless practice + LAN security preview · L12 — IP fundamentals & ARP |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO7|L11]** Give the security rationale (one sentence) for placing guest Wi-Fi
clients in their own VLAN with no route to staff networks.

**Q2 [I|CLO3|L12]** Split 192.168.4.0/24 into four equal subnets. Give the new prefix
length, each subnet's address range, and usable hosts per subnet.

**Q3 [I|CLO4|L12]** Walk through ARP resolution for host A (10.0.0.5/24) reaching
10.0.0.9: what is broadcast, what is cached, and what prevents every host from
answering?

**Q4 [I|CLO4|L12]** Host A (10.0.0.5/24, gateway 10.0.0.1) sends to 203.0.113.7. What
destination MAC address does A's frame carry, and why not 203.0.113.7's MAC?

**Q5 [I|CLO2|L11]** In a multi-AP building, why is setting neighboring APs to the *same*
2.4 GHz channel harmful, and which channel plan does the course recommend?

**Q6 [I|CLO3|L12]** Is 192.168.4.197 inside 192.168.4.192/26? Show the mask reasoning.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Guest devices are untrusted: isolating their VLAN (plus firewall rules) contains
sniffing, ARP/flooding attacks, and lateral movement so a compromised guest cannot reach
staff systems. [B·CLO7]

**Q2.** /26 each: **192.168.4.0–63**, **.64–127**, **.128–191**, **.192–255**; 62 usable
hosts per subnet (network + broadcast reserved) [MC]. [I·CLO3]

**Q3.** A broadcasts an ARP *request* ("who has 10.0.0.9?") to ff:ff:ff:ff:ff:ff; only
the owner of 10.0.0.9 replies (its own MAC) — other hosts may cache the sender
(10.0.0.5 ↔ MAC) pair but do not answer. A caches the reply pair; expiry/refresh per
stack policy. [I·CLO4]

**Q4.** The frame's destination MAC is the **default gateway's** MAC (A ARPs for
10.0.0.1). 203.0.113.7 is off-subnet, so MAC resolution is only meaningful on the local
link; IP routing carries the packet onward, and the destination IP in the header
remains 203.0.113.7. [I·CLO4]

**Q5.** Co-channel contention: same-channel APs and their clients share airtime (CSMA),
so they must take turns even when they could not directly help each other — throughput
collapses toward a shared budget. Recommended plan: non-overlapping channels 1, 6, 11. [I·CLO2]

**Q6.** /26 mask = 255.255.255.192; network = 192.168.4.192, broadcast = .255, range
.192–.255. 197 ≥ 192 and ≤ 255 → **yes, inside** [MC]. [I·CLO3]
