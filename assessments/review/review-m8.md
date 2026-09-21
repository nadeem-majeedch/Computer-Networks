# Module 8 Review Questions (L30–L32)

| Field | Value |
|---|---|
| Coverage | L30 mobile & wireless enterprise networking · L31 enterprise design & data-science connection · L32 capstone workshop & synthesis |
| Use | Self-study after each lecture; answers in the key below |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · Capstone: CS-04 · Cases PB-059…PB-065 |

## Questions

### L30 — Mobile & wireless enterprise networking
1. [B|CLO6] Name the two RF planning quantities a WLAN designer balances when placing
   APs (coverage vs capacity).
2. [I|CLO6] A warehouse office has strong signal everywhere and 60 users on one AP.
   Diagnose and fix in two sentences.
3. [I|CLO6] Roaming handshake: why can a client's roam between two same-channel APs
   still drop VoIP frames, and what design reduces the gap?

### L31 — Enterprise design & the data-science connection
4. [I|CLO6] Give the enterprise design document's five required sections (course
   version) and the one artifact each produces.
5. [I|CLO5] Nightly 2 TB dataset sync on a 10 Gb/s path, 20 ms RTT: minimum time and
   the two tuning levers if real time is 4× the minimum?
6. [I|CLO6] Model serving latency spikes at 09:00. Which two network measurements
   separate "link problem" from "server problem," and where do you measure each?

### L32 — Capstone workshop & synthesis
7. [I|CLO8] List the capstone's five deliverables (course version) and the weight of
   each within the 15%.
8. [I|CLO6] Design review: an examiner asks "what happens when the core switch dies?"
   Which two capstone artifacts answer it, and how?
9. [E|CLO8] Synthesis: trace one HTTPS request from a staff laptop to an internal
   server across every layer *and* every policy point (VLAN, firewall, DNS) — name
   each decision point in order.

---

## SELF-CHECK KEY — attempt first, then verify

1. Coverage: signal/SNR footprint per AP. Capacity: aggregate client demand vs radio
   airtime. Design balances both — enough APs that no cell is overloaded.
2. Diagnosis: airtime contention, not coverage — 60 clients share one radio. Fix:
   add APs on non-overlapping channels (split the cell), or move clients to 5/6 GHz.
3. The roam itself requires reassociation (and channel change if channels differ);
   frames in flight during that window are lost unless the design keeps buffer/
   forwarding continuity (fast transition, same-channel overlap, or key caching).
4. Requirements (scope/hosts table) → addressing plan (VLSM sheet) → topology
   (L2/L3 diagram) → services & policy (DHCP/DNS/firewall matrix) → verification plan
   (test/measurement list). One artifact per section.
5. 2 TB = 1.6×10¹³ bits ÷ 10¹⁰ b/s = **1600 s ≈ 26.7 min** [MC]. Levers: TCP window
   scaling/app (UDT/aria2-class parallelism) to fill the 20 ms BDP (25 MB), and
   fewer/larger files (round-trip amortization).
6. Separation: (i) RTT/loss between client and server *network path* (ping/mtr from
   client at 09:00 vs baseline) vs (ii) server response time (app server metric or
   TCP handshake timing server-side). Path metric normal + server metric spiked →
   server problem, and vice versa.
7. Design document 25% · build demo 20% · monitoring dashboard + data 20% · final
   report 20% · defense 15% (within the 15% course weight — strategy §3.7).
8. Design document: the redundancy section (STP/uplink plan, failover IP). Monitoring
   dashboard: recorded failover test showing convergence time and loss during the
   event. Either artifact answers "what happens" with evidence.
9. Order: app resolves name (DNS via VLAN-permitted resolver) → client ARP for gateway
   (its VLAN) → firewall/router policy check inter-VLAN (permit 443 to servers) →
   TCP handshake across routed path → TLS to the *named* server (cert chain) →
   HTTP request served. Each named point (DNS, ARP/gateway, VLAN policy, routing,
   TLS) earns a share; the skill is *ordering*, not prose.
