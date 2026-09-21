# Midterm Examination — Student Paper

| Field | Value |
|---|---|
| Course | Computer Networks — Midterm (Modules 1–3: L01–L16) |
| Duration / marks | **90 minutes · 60 marks** (Section A 18 · B 24 · C 18) |
| Aids | Formula sheet provided (last page) · non-programmable calculator ⚠ per university rules · **no devices** |
| Integrity | Individual, closed-book — [`../academic-integrity.md`](../academic-integrity.md) §4 |
| Evidence note | Packet excerpts in Section C are **synthetic, written for this exam, internally consistent** |

Answer **all** questions in the answer booklet. Show working: method marks are
awarded even when arithmetic fails. State assumptions on numerical items.

## Section A — Selected response & short answer (18 marks)

**A1–A6 (1 mark each).** Circle one answer.

**A1.** The transport layer hands the internet layer its PDU called:
(a) frame (b) segment (c) datagram (d) message

**A2.** An 802.1Q tag is inserted:
(a) before the destination MAC (b) after the source MAC (c) inside the payload
(d) in the FCS

**A3.** Traceroute's per-hop replies are:
(a) ICMP Echo Reply (b) ICMP Time Exceeded (c) ICMP Destination Unreachable
(d) TCP RST

**A4.** NAT on a home router primarily rewrites:
(a) MAC addresses (b) IP/port fields in headers (c) payload checksums
(d) routing tables

**A5.** `fe80::1` is:
(a) a global unicast (b) a multicast (c) a link-local unicast (d) a ULA

**A6.** A switch receives a unicast frame whose destination MAC is not in its table.
It:
(a) drops it (b) floods it in its VLAN except the ingress port (c) sends it to the
router (d) returns it to sender

**A7 (2).** Explain why full-duplex switched Ethernet makes CSMA/CD unnecessary.

**A8 (2).** Distinguish a collision domain from a broadcast domain with one example
of each boundary.

**A9 (2).** State one error pattern an internet checksum can miss that a CRC catches,
and why.

**A10 (2).** In DHCP's DORA, which message must be broadcast and why? One sentence.

**A11 (2).** Define longest-prefix match in one sentence and state what a default
route's prefix length is.

**A12 (2).** Live audio streams choose UDP. State the property that drives the choice
and the cost the application accepts.

## Section B — Problems (24 marks)

**B1 — Addressing (8).** Given `10.30.0.0/22`:
(a) usable host addresses (1)
(b) split into four equal subnets: prefix + ranges (2)
(c) smallest prefix for 90 hosts (1)
(d) which of your four subnets contains 10.30.3.200 (1)
(e) /22 mask in dotted-decimal (1)
(f) aggregate 10.30.0.0/22 and 10.30.4.0/22 into one prefix, and state the condition
that makes the summary safe (2)

**B2 — Capacity & delay (8).** A 2 MB file crosses an idle 20 Mb/s link; RTT 60 ms;
one setup RTT precedes data.
(a) transfer time ignoring setup and propagation (2)
(b) total time including the setup RTT (2)
(c) Shannon ceiling of a 1 MHz channel at SNR = 20 dB (linear SNR ≈ 100;
log₂101 ≈ 6.66) (2)
(d) one-way propagation over 300 km of fiber (2×10⁸ m/s) (2)

**B3 — Switching & routing (8).**
(i) A switch's table is empty. Host A (port 1, MAC a1) sends a frame to MAC m9;
m9 (port 3) replies. Write the table's contents after both frames, with each entry's
trigger. (4)
(ii) R has: `10.0.0.0/8 → R1` · `10.4.0.0/16 → R2` · `10.4.8.0/24 → local`.
State the next hop for 10.4.8.7, 10.4.9.1, 10.7.2.2, and name the deciding rule. (4)

## Section C — Trace analysis (18 marks)

**C1 (9).** Excerpt (synthetic):

```text
dst MAC  = 0c:5b:8f:1a:00:01    src MAC = 9c:b6:d0:aa:bb:17
type = 0x0800   IP src = 10.20.1.35   IP dst = 198.51.100.9
ttl = 62   proto = 6   TCP 51002 → 443 [SYN] seq=0
```

The campus gateway's MAC is 0c:5b:8f:1a:00:01.
(i) Which device originated the frame, and how do you know? (2)
(ii) Why does the destination MAC differ from the IP destination's "owner"? (2)
(iii) How many routers did the packet cross before this point? Justify. (2)
(iv) The campus egress NATs this flow. State what changes in the packet at egress and
what state is recorded. (3)

**C2 (9).** Excerpt (synthetic):

```text
t=0.000  10.1.1.5:51000 → 198.51.100.9:443  [SYN]     seq=3000
t=0.055  198.51.100.9:443 → 10.1.1.5:51000  [SYN,ACK] seq=8000 ack=3001
t=0.056  10.1.1.5:51000 → 198.51.100.9:443  [ACK]     seq=3001 ack=8001
t=0.057  10.1.1.5:51000 → 198.51.100.9:443  [PSH,ACK] seq=3001 len=1000
```

(i) Compute the RTT, naming the packet pair used. (2)
(ii) The server's next ACK carries which number, and what does it assert? (3)
(iii) The capture ends at t=0.200 with no server response. Give one hypothesis the
excerpt supports and one it does **not** (with a reason each). (4)

---

*Formula sheet (provided):* Nyquist C = 2B log₂M · Shannon C = B log₂(1+SNR) ·
SNR(dB) = 10 log₁₀(SNR) · serialization = bits/link-rate · usable hosts = 2^h − 2 ·
rate ≈ window/RTT
