# Lecture 07 — Instructor Teaching Notes
## MAC Protocols & Wired LANs: Ethernet (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO2 primary; CLO4 frame analysis |
| Textbook anchor | PD §2.6 |

---

## 1. Objectives hook
Board: **"1973: one cable, 100 computers, no referee. Every host talks when it wants.
Design a rule so this works."**

Hook (2 min): classroom-air analogy — if 60 people share one microphone, what rules could
work? (Wait turns / talk only if quiet / detect collisions and back off.) Those are exactly
the MAC protocol families.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L06 stuffing recall; microphone analogy |
| 6–26 | Concept 1 | Multiple access: ALOHA → CSMA → CSMA/CD; efficiency math |
| 26–42 | Concept 2 | Ethernet evolution: 10Base5 → hubs → switches; full duplex |
| 42–55 | Concept 3 | Ethernet II frame anatomy, field by field |
| 55–60 | Break | — |
| 60–80 | GA-07 | Wireshark frame dissection, pairs |
| 80–95 | Worked examples | Efficiency numbers; MTU/overhead; jumbo frames (enr) |
| 95–108 | Discussion | Why collisions died: economics of switching |
| 108–118 | Summary + exit ticket | — |
| 118–120 | Preview | Switches: what the box actually does (L08) |

## 3. Concept walkthrough

### 3.1 The multiple-access problem & protocol evolution (20 min)
- **The problem:** a shared broadcast medium, distributed users, no central scheduler —
  how to share without (much) coordination?
- **ALOHA (1970s, Hawaii):** transmit whenever; on collision (no ack), wait random time,
  retry. Pure ALOHA max utilization ≈ 18%. **Slotted ALOHA:** transmit only on slot
  boundaries → ≈ 37%. Beautiful first lesson: *order buys throughput*.
- **Carrier Sense (CSMA):** listen before talking — don't start into an ongoing
  conversation. Still fails: **propagation delay** means two hosts can both sense "idle"
  and collide anyway (draw the two-hosts-far-apart collision diagram).
- **CSMA/CD (collision detection):** while transmitting, also *listen*; on collision,
  abort, send jam signal, **binary exponential backoff** (wait k×slot-time, k drawn from
  0..2^i−1 after i collisions). Classic Ethernet (10BASE5/10BASE2, hubs) used this.
- **Efficiency intuition (simplified model):** performance depends on the ratio of
  propagation time to transmission time (a/RTT-style ratio); Ethernet's 64-byte minimum
  frame exists *because* CSMA/CD must still be transmitting when the collision comes back
  (64 bytes @ 10 Mbps ≈ 51.2 µs ≥ 2×max propagation of 2500 m) — a gorgeous "the standard
  is physics made policy" example.
- **The end of collisions:** switches give each host its own collision domain; full-duplex
  twisted pair has separate TX/RX pairs → no collisions possible → CD disabled. Modern
  Ethernet (1G+) is *always* switched full-duplex; CSMA/CD survives only as history.
- Simplified teaching model flag: modern PHYs (OFDM etc.) differ from the classic
  backoff-era radios; wireless carriers (CSMA/CA) are L10's topic.

### 3.2 Ethernet evolution (16 min)
- 1973 Metcalfe memo → 10 Mbps 10BASE5 ("thicknet", vampire taps) → 10BASE2 thinnet →
  10BASE-T twisted pair + **hubs** (physical-layer repeaters: one collision domain) →
  **switches** (L2 forwarding: each port its own collision domain) → 100M → 1G → 10G →
  25/40/100/400G in data centres.
- Hubs vs switches (crucial distinction, exam favorite): hub = broadcast electrical
  signal to all ports (L1); switch = receives full frame, forwards selectively (L2,
  store-and-forward — connecting back to L06's framing).
- Full duplex doubles effective capacity and ends CSMA/CD; auto-negotiation picks speed
  and duplex.
- Broadcast vs collision domains (define now; L08 exercises them): every switch port =
  own collision domain; the whole VLAN/LAN is still ONE broadcast domain (until L09
  fixes that).

### 3.3 Ethernet II frame anatomy (17 min)
| Field | Size | Purpose |
|---|---|---|
| Preamble + SFD | 7+1 B | Physical sync (not counted in "frame" by most tools) |
| Destination MAC | 6 B | Target NIC (unicast/multicast/broadcast ff:ff:ff:ff:ff:ff) |
| Source MAC | 6 B | Sender NIC |
| EtherType | 2 B | Which L3 payload? 0x0800 IPv4, 0x0806 ARP, 0x86DD IPv6 |
| Payload | 46–1500 B | L3 packet; min size via padding to reach 64 B frame |
| FCS (CRC-32) | 4 B | L06's error detection (usually invisible in Wireshark) |
- MAC address structure: 48 bits, OUI (vendor prefix, first 3 bytes) + NIC-specific;
  burnedin vs spoofable (settable in software — ethics note + L11 preview).
- MTU 1500: historical; jumbo frames (9000) in DCs (enr); interplay with IP fragmentation
  (preview: L12/L18 handle what happens when a packet exceeds it).
- Frame efficiency: payload/(payload+overhead) — 1500/1538 ≈ 97.5%; at 64 B: 46/72 ≈ 64%
  (why small packets are "expensive" per byte — connects to L04's iperf numbers).

### Reference diagram — Ethernet II frame layout

```text
┌──────────┬─────────┬─────────┬──────┬───────────────────┬─────┐
│ preamble │ dst MAC │ src MAC │ type │ payload 46–1500 B │ FCS │
│    8 B   │   6 B   │   6 B   │ 2 B  │                   │ 4 B │
└──────────┴─────────┴─────────┴──────┴───────────────────┴─────┘
 minimum frame (no preamble) = 6+6+2+46+4 = 64 B
```

## 4. Important definitions
Multiple-access protocol · ALOHA (pure/slotted) · CSMA · CSMA/CD · Binary exponential
backoff · Jam signal · Collision domain · Broadcast domain · Hub vs switch · Full duplex ·
MAC address · OUI · EtherType · MTU · Preamble/SFD · FCS · Auto-negotiation.

## 5. Real-world examples
- **The 64-byte minimum** as fossil: a rule born of 10 Mbps coax physics still living in
  your 1G dorm port — standards' archaeology made tangible.
- **OUI lookup:** first 3 bytes of your laptop's MAC identify the vendor (do a live lookup
  on a student's MAC via the IEEE OUI registry) — also why MAC randomization exists for
  privacy (phones rotate Wi-Fi MACs; link it to L11 security).
- **Why your "1 Gbps" office port shows 1.0 Gb/s full duplex in `ip link`:** auto-negotiation
  result — students can check on the VM.

## 6. Mathematical/technical example
1. Slotted vs pure ALOHA utilization (state the numbers; no derivation): 37% vs 18% —
   doubling from ordering alone.
2. Minimum frame & propagation: 10 Mbps, 64 B → 51.2 µs transmission; 2×2500 m/2×10⁸ =
   25 µs round trip — the standard's numbers interlock (simplified model).
3. Efficiency: 1500 B payload over 1 Gbps: frame 1538 B on wire → 97.5% top efficiency;
   small-packet penalty math (64 B → 64%).

## 7. GA-07: frame dissection in Wireshark (20 min)
Worksheet: given a real capture excerpt (provided), students: identify DA/SA, classify the
destination address type, decode EtherType, extract payload length, compute efficiency %,
and answer "what would a hub do with this frame? what would a switch do?" (Bridges into
L08.) Filter used: `eth` / `eth.type == 0x0800`.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Switches are just fast hubs" | Hub = L1 repeater (one collision domain); switch = L2 store-and-forward per-port |
| "CSMA/CD still runs on modern Ethernet" | Full duplex switched links have no collisions to detect |
| "MAC addresses are globally unique and immutable" | Spoofable in software; randomized for privacy; only locally significant |
| "Ethernet frame includes the preamble" | Preamble/SFD are physical-layer sync; Wireshark shows frame from DA |
| "Broadcast and collision domains are the same" | One switch = many collision domains, one broadcast domain (VLANs change this — L09) |
| "1 Gbps port = 1 Gbps goodput" | Overhead math (97.5% ceiling) + L04's iperf numbers |

## 9. Suggested practical demonstration
On the VM: `ip link` (show state/speed/duplex/MTU); Wireshark capture of one `ping` —
identify ARP request broadcast (ff:ff:ff:ff:ff:ff — teaser for L12) then ICMP frames;
show `ethtool` speed/duplex report. ⚠ Pre-verify all three commands on the image.

## 10. Classroom activities
- **ALOHA efficiency bet:** before revealing numbers, pairs bet whether pure ALOHA tops
  at 5/18/50/90% — reveal, then discuss *why* order wins.
- **Frame puzzle:** hand out a hex dump; first pair to correctly label all fields wins.
  (Same worksheet as GA-07 part A; gamify it.)

## 11. Problem-solving questions
1. Why must the minimum frame size grow with network diameter (in CSMA/CD systems)?
2. Compute efficiency for a 100-byte payload Ethernet frame.
3. A hub receives a frame for MAC X on port 3. What does it do? A switch (with X learned
   on port 3)? (Preview of L08.)
4. EtherType 0x86DD = ? 0x0806 = ?
5. Why does full-duplex Ethernet double capacity versus half-duplex at the same rate?

## 12. Formative assessment (with answers)
- MCQ: Binary exponential backoff after the 3rd collision draws k from → **0..7**.
- MCQ: ff:ff:ff:ff:ff:ff is → **broadcast**.
- MCQ: Which field does the receiver use to hand the payload to IPv4? → **EtherType**.
- Short: why did switches kill collisions? → per-port collision domains + full duplex.

## 13. Exit ticket
1. Order the evolution: hubs / thicknet / switches / thinnet: ________
2. EtherType for IPv4: ________
3. One collision domain per ________ (hub/switch port?).

## 14. Anticipated difficulties
- Students conflate collision domain with broadcast domain: use the "switch = apartment
  building (private halls), VLAN = building" metaphor; formalize at L08/L09.
- Hex reading anxiety in GA-07: provide a labeled template on the worksheet.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify Wireshark trace with clean Ethernet II frames is on the podium VM
- [ ] Prepare hex-dump handouts (GA-07); test `ethtool`/`ip link` output
- [ ] IEEE OUI registry tab open for the live vendor lookup
- [ ] Board pre-write: evolution timeline; frame field table skeleton

## 16. Timing fallbacks
Drop ALOHA bet activity and jumbo frames (enr); protect GA-07 and frame anatomy — the
dissection skill is assessed and reused in every later packet lab.

## 17. References
- PD §2.6; Tanenbaum MAC/Ethernet sections (⚠ verify).
- IEEE 802.3 standard (frame format; cite the standard, don't distribute it).
- Metcalfe & Boggs, "Ethernet: Distributed Packet Switching for Local Computer Networks"
  (1976) — historical origin.
- IEEE OUI registry (standards.ieee.org) for the vendor-lookup demo.
- ⚠ VERIFY edition/sections this semester.
