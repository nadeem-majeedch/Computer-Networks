# Module 2 Review Questions (L05–L11)

| Field | Value |
|---|---|
| Coverage | L05 physical · L06 framing/CRC · L07 Ethernet · L08 switching · L09 VLANs · L10 Wi-Fi fundamentals · L11 wireless practice & LAN security preview |
| Use | Self-study after each lecture; answers in the key below |
| Links | Lecture packages: [`../../lectures/`](../../lectures/) · LAB-02/03 · Cases PB-009…PB-022 |

## Questions

### L05 — Physical layer
1. [I|CLO2] Channel: 4 kHz, 16 levels, noiseless. Maximum bit rate? Which law?
2. [I|CLO2] Same channel at SNR 20 dB: what does Shannon cap, and which law now binds?
3. [B|CLO2] Give one application where fiber is mandatory *besides* distance, and the
   physical property that forces it.

### L06 — Framing, errors & reliability
4. [B|CLO2] Why do protocols need *framing* at all — what breaks without it?
5. [I|CLO2] A CRC-8 catches all bursts ≤ 8 bits. Explain in one sentence why bursts
   longer than 8 can also be caught.
6. [I|CLO2] Satellite link, 600 ms RTT, BER 10⁻⁶: argue ARQ vs FEC for bulk science
   data.

### L07 — Ethernet
7. [B|CLO4] Name the Ethernet frame fields between destination MAC and payload, and
   the one value EtherType commonly takes for IPv4.
8. [I|CLO2] Why does a switch's full-duplex port make the CSMA/CD algorithm dead code
   on that port?
9. [I|CLO4] 1518-byte frame on a 10 Gb/s link: serialization time (2 sf is fine).

### L08 — Switching & LAN design
10. [I|CLO2] State the three FDB operations a switch performs on any arriving frame.
11. [I|CLO6] Hierarchy question: why do campus designs keep broadcast domains small
    (per-floor VLANs) instead of one big flat Layer 2?
12. [I|CLO6] Two switches connected by two cables form a loop. What problem arises
    before any configuration, and which protocol's *purpose* (not mechanics) fixes it?

### L09 — VLANs
13. [B|CLO2] Access port vs trunk port: tagging behavior of each in one sentence.
14. [I|CLO6] Give the two inter-VLAN design consequences of putting each department in
    its own VLAN (routing + security).
15. [I|CLO2] Voice + data on one access port: how do phones tag, and why does that
    differ from the PC's frames?

### L10 — Wi-Fi fundamentals
16. [B|CLO2] Why does Wi-Fi use CSMA/CA (avoidance) rather than CSMA/CD (detection)?
17. [I|CLO4] SSID, BSSID, ESS: define each in one line and give the roaming unit
    between APs.
18. [I|CLO2] 2.4 GHz plan with channels 1, 6, 11: what does "non-overlapping" protect?

### L11 — Wireless practice & LAN security preview
19. [I|CLO6] A site survey shows −55 dBm everywhere but users complain. Name the
    measurement that RSSI misses and one tool check.
20. [I|CLO7] What is a rogue AP, and what is the classic defense?
21. [I|CLO7] What does 802.1X authenticate that WPA2-PSK cannot, and what replaces the
    shared password?

---

## SELF-CHECK KEY — attempt first, then verify

1. Nyquist: 2·4000·log₂16 = 8000·4 = **32 kb/s** [MC].
2. Shannon: C = 4000·log₂(1+100) ≈ 4000·6.66 ≈ **26.6 kb/s** [MC] — Shannon now binds
   (Nyquist allows more, noise forbids it).
3. Electromagnetic-interference environments (factories, near motors/rails): fiber
   carries light, not charge, so induced noise cannot corrupt it.
4. Without framing the receiver cannot find message boundaries in the bit stream —
   payload, addressing, and error checks all need delimited frames.
5. The polynomial property guarantees detection of *all* bursts shorter than the degree;
   longer bursts fail detection only if the error pattern is divisible by the generator
   (probability falls off rapidly) — hence "also" not "always."
6. FEC: fix errors locally, avoid 600 ms-per-retry round trips — better for bulk data
   when error rate is moderate. ARQ wastes 600 ms per lost block. Hybrid acceptable.
7. Source MAC, EtherType/Length (then optional 802.1Q); EtherType 0x0800 = IPv4.
8. Separate transmit/receive pairs to a switch: no shared medium, no collision to
   detect — carrier sense has nothing to arbitrate.
9. 1518·8 bits / 10¹⁰ b/s ≈ **1.21 µs** [MC].
10. Learn source MAC ↔ port; forward/filter by destination lookup; flood if unknown
    (and age entries).
11. Broadcast traffic (ARP, DHCP, discovery) scales with hosts in the domain; small
    domains bound the blast radius of both load and L2 attacks.
12. A loop causes frame storms/broadcast multiplication and FDB flapping; the
    spanning-tree protocol's purpose is to detect loops and logically block redundant
    links while keeping a loop-free connected graph.
13. Access: untagged frames mapped to one VLAN; trunk: tagged frames for many VLANs.
14. Routing: inter-department traffic must traverse an L3 device (subnets per VLAN).
    Security: policy enforcement point at that router/firewall — lateral movement is
    no longer free.
15. The phone tags its frames with a voice VLAN ID (802.1p/Q); the PC's frames stay
    untagged into the data VLAN — different QoS and security treatment.
16. A radio cannot transmit and listen simultaneously on one channel — collision
    *detection* is physically unreliable, so Wi-Fi avoids collisions via listen-before-
    send + random backoff.
17. SSID: network name; BSSID: one AP radio's MAC; ESS: all APs sharing one SSID.
    Roaming unit = BSS (AP cell): the client re-associates to a new BSSID.
18. It prevents adjacent-channel overlap: 1/6/11 are spaced 5 channels apart, so
    neighboring APs' transmissions do not partially overlap and corrupt each other's
    frames.
19. SNR (signal *relative to noise floor*) and channel utilization — RSSI alone ignores
    noise/interference; check spectrum/channel-usage tools and AP load stats.
20. An unauthorized AP (often bridging trusted LAN); defense: 802.1X/NAC so unknown
    devices fail port authentication, plus rogue-AP detection (WIDS).
21. 802.1X authenticates the *user/device* (supplicant→authenticator→RADIUS) per
    identity; per-session keys (from EAP-derived material) replace the shared PSK,
    so credentials are individual and revocable.
