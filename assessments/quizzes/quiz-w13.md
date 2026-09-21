# Weekly Quiz — Week 13 (L25, L26)

| Field | Value |
|---|---|
| Coverage | L25 — Firewalls, segmentation & VPNs · L26 — Attack & defense case workshop |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | **Graded-quiz candidate window** (strategy §2; see assessments/README.md §5 reconciliation note) |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO7|L25]** State what a stateless packet filter can decide from one packet
alone, and one attack class that only *stateful* inspection stops.

**Q2 [I|CLO7|L25]** Rule list (top-first match): (1) deny 10.9.0.0/16 → 10.9.5.0/24:22;
(2) allow 10.9.0.0/16 → 10.9.5.0/24:any. An admin in 10.9.2.8 connects to 10.9.5.1:22 —
result, and which rule decides?

**Q3 [I|CLO7|L25]** A site-to-site VPN joins HQ (10.20.0.0/22) and branch (10.30.0.0/24).
Which subnets must the VPN policy include, and what stays unencrypted on the public path?

**Q4 [B|CLO7|L26]** In defense-in-depth terms, classify: (i) staff security training,
(ii) switch port VLAN assignment, (iii) TLS to the web server. One layer name each.

**Q5 [I|CLO6|L26]** A workstation got a spoofed "bank" email and the user typed
credentials. Name the attack, and give one network-layer control and one
human-layer control that mitigate it.

**Q6 [I|CLO6|L26]** During the workshop your lab subnet shows ARP replies from three
different MACs for one IP. Which attack does the scenario suggest, and which L26
defense applies?

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Stateless: per-packet header test only (addresses, ports, flags) against static
rules. Stateful requirement example: detecting/allowing an *established* TCP flow's
return traffic (or dropping unsolicited inbound packets that merely *pretend* to be
replies — forged-ACK class attacks). [B·CLO7]

**Q2.** **Denied** — rule (1) matches first; packet filters apply first-match, so the
broader allow in (2) never sees the packet. Classic ordering pitfall. [I·CLO7]

**Q3.** Policy must include both protected subnets (10.20.0.0/22 ↔ 10.30.0.0/24) as
tunnel selectors. On the public path only the *outer* tunnel headers (public IPs,
VPN protocol) stay visible — inner packets are encrypted; still, the outer headers
reveal that the two sites communicate. [I·CLO7]

**Q4.** (i) Human/awareness layer · (ii) Network-access/Layer-2 control (segmentation)
· (iii) Application/transport-layer cryptographic control. Any consistent
defense-in-depth naming accepted. [B·CLO7]

**Q5.** Phishing (credential harvesting). Network-layer: mail filtering/DMARC-based
rejection, or block known-bad destinations (limited — say so). Human-layer: training +
report-button culture, phishing simulations. [I·CLO6]

**Q6.** ARP spoofing/poisoning (three MACs claiming one IP). L26 defenses: dynamic ARP
inspection (switch validates bindings), or static ARP entries on critical pairs, or
port security — any switch-enforced binding validation accepted. [I·CLO6]
