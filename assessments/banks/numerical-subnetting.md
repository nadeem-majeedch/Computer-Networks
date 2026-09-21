# Question Bank — Numerical & Subnetting

| Field | Value |
|---|---|
| Scope | Addressing/VLSM design, capacity math, delay budgets, transport windows, airtime |
| Tagging | `[Difficulty|CLO|Source]`; all numeric answers marked **[MC]** = script-verified (`tools/scripts/verify_assessment_numbers.py`) |
| Key | fenced at end — do not distribute |
| Standards note | /31 point-to-point convention is RFC 3021; Shannon/Nyquist as taught in L05 |

## Questions

**N-01 [B|CLO3|L13]** Usable hosts in a /26? In a /27?

**N-02 [I|CLO3|L13]** For 172.16.20.77/28 give: network, broadcast, usable range, mask.

**N-03 [I|CLO3|L13]** How many /25 subnets carve a /16? What changes if the requirement
is "each /25 must keep 2 spare addresses beyond its 126 hosts"?

**N-04 [I|CLO3|L13]** Aggregate 192.168.16.0/24 through 192.168.31.0/24 into one
summary prefix. Why is the summary safe only if no exceptions exist?

**N-05 [A|CLO3|L13/L16]** From 10.200.0.0/21 allocate, largest-first, exact-fit-or-next:
500, 200, 100, 50 hosts; then two /30 router links. List every prefix with range, and
the remaining free block.

**N-06 [I|CLO5|L04]** Minimum transfer time for 250 GB across an idle 1 Gb/s path?

**N-07 [I|CLO5|L01/L05]** Propagation floor: 5 000 km of fiber, light speed in glass
≈ 2×10⁸ m/s. One-way delay and RTT floor (electronics ignored)?

**N-08 [I|CLO5|L19]** BDP of 10 Gb/s at 40 ms RTT, in MB. What receiver window keeps
the pipe full?

**N-09 [I|CLO5|L07]** Serialization time of a 1 500 B frame at 100 Mb/s and at 1 Gb/s.

**N-10 [A|CLO2|L05]** Shannon ceiling of a 10 MHz channel at SNR = 15 dB (linear SNR
≈ 31.6; log₂(32.6) ≈ 5.03).

**N-11 [I|CLO3|L13]** Is 10.20.30.44 inside 10.20.30.32/27? Show the range.

**N-12 [B|CLO3|L13]** How many /29 subnets fit in a /26?

**N-13 [I|CLO3|L15]** Compress 2001:0db8:0000:0001:0000:0000:0000:00ff per RFC 5952.

**N-14 [I|CLO4|L18]** Handshake with client ISN 5000, server ISN 9000; client then
sends 200 B. What is the server's next ACK number, and what does it assert?

**N-15 [I|CLO5|L03]** A 5 MB fetch over 100 Mb/s, RTT 30 ms, with 2 setup RTTs (TCP +
TLS) before data. Total minimum time.

**N-16 [I|CLO3|L22]** A DHCP scope serves 10.1.6.0/23 with 10 addresses reserved for
printers. Maximum dynamic clients?

**N-17 [I|CLO5|L01]** Store-and-forward: a 1 500 B frame crosses three hops, all
1 Gb/s, propagation negligible. Minimum end-to-end serialization delay.

**N-18 [I|CLO6|L10]** One AP delivers 100 Mb/s of airtime goodput, fairly shared by
five active clients. Per-client share, and the name of the limiting resource.

**N-19 [I|CLO5|L01/L04]** A 1 Gb/s egress receives a burst of 100 × 1 500 B frames
from a 100 Mb/s ingress. How long does the burst take to drain, and what does the
queue's existence prove?

**N-20 [I|CLO4|L07/L18]** Efficiency of a full-size Ethernet frame carrying a 1 460 B
TCP payload (20 B TCP + 20 B IP + 18 B Ethernet overhead): percent payload.

**N-21 [I|CLO4|L14]** NAT capacity: 300 clients × 50 concurrent flows each; 4 public
IPs; ~64 000 usable ports per IP. Mapping capacity and margin.

**N-22 [A|CLO3|L13/L31]** A /22 serves 800 hosts today. Does it survive 3 years at
20%/yr growth? At 40%/yr? State the prefix change if any.

**N-23 [I|CLO6|L01/L31]** One-way delay budget: application ceiling 100 ms; measured
propagation 60 ms; serialization 0.12 ms. What margin remains for queueing + processing,
and what does the design do if it's negative?

**N-24 [I|CLO5|L04]** `iperf3` shows 9.4 Gb/s on a 10 Gb/s link. Overhead percent, and
one legitimate cause it may include.

**N-25 [E|CLO3|L13/L16]** Design from 172.16.0.0/16: 8 buildings × ≤ 500 hosts each,
12 point-to-point links, and one /28 future reserve per building. Choose per-building
and per-link prefixes so the whole plan fits in **one /20 plus two small blocks**, the
building over-provision is ≤ 2%, and show one fully worked building (range + waste).

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE (all [MC] unless noted)

**N-01.** /26 → 62; /27 → 30. **N-02.** Network 172.16.20.64/28; broadcast .79;
usable .65–.78; mask 255.255.255.240. **N-03.** 512 subnets. Spare-address requirement
changes nothing arithmetically (126 usable already exceeds 124) — the trap is assuming
spares shrink the prefix. **N-04.** 192.168.16.0/20 (16 contiguous /24s = exactly the
/20's span). Safe only with no exceptions: any covered route announced more
specifically elsewhere wins by longest-prefix match and can blackhole via the summary
if the summary is used without the specifics. **N-05.** 10.200.0.0/23 (500≤510;
usable .0.1–.1.254) · 10.200.2.0/24 (200≤254; .2.1–.2.254) · 10.200.3.0/25 (100≤126;
.3.1–.3.126) · 10.200.3.128/26 (50≤62; .3.129–.3.190) · 10.200.3.192/30 (.3.193–.194) ·
10.200.3.196/30 (.3.197–.198). Free: 10.200.3.200 – 10.200.7.255. **N-06.** 250 GB = 2.5×10¹¹ B = 2×10¹² bits; ÷10⁹ b/s = **2 000 s ≈ 33.3 min**. **N-07.** 5×10⁶ m ÷ 2×10⁸
m/s = 25 ms one-way; **50 ms RTT** (floor — real paths add per-hop processing/queueing).
**N-08.** 10¹⁰ × 0.04 = 4×10⁸ bits = 50 MB; window ≥ 50 MB (plus headroom for
efficiency). **N-09.** 12 000 bits ÷ 10⁸ = 120 µs; ÷ 10⁹ = 12 µs. **N-10.** C = 10×10⁶
× 5.03 ≈ **50.3 Mb/s**. **N-11.** /27 range .32–.63; 44 ∈ [32,63] → **yes**. **N-12.**
8 (26÷3 bits: 64/8). **N-13.** 2001:db8:0:1::ff (drop leading zeros; one `::` for the
longest all-zero run — here the three zero groups). **N-14.** ACK = **5201** [seq
5000+1(SYN)+200]: "next expected byte is 5201." **N-15.** Data 5×8×10⁶ ÷ 10⁸ = 0.4 s;
setup 2×30 ms = 0.06 s → **0.46 s**. **N-16.** /23 = 512 − network − broadcast = 510
usable; −10 printers → **500** dynamic clients. **N-17.** 3 × 12 µs = **36 µs**
(store-and-forward repeats serialization per hop). **N-18.** 100÷5 = **20 Mb/s**;
limiting resource = radio **airtime**. **N-19.** 100×12 000 bits ÷ 10⁹ = **1.2 ms**
drain; queue existence proves ingress demand > egress capacity in that instant —
queueing delay is load-dependent (L01 taxonomy). **N-20.** 1 460 ÷ 1 518 ≈ **96.2%**.
**N-21.** 4 × 64 000 = 256 000 mappings vs 15 000 needed → margin ≈ 17×; note real
limits also include per-flow state timeouts. **N-22.** 20%/yr: 800×1.2³ ≈ 1 382 hosts — /22 (1 022 usable) is already too small;
**/21** (2 046) suffices. 40%/yr: 800×1.4³ ≈ 2 195 > 2 046 → **/20** (4 094). The
common error is planning on the current count without compounding. **N-23.** 100 − 60 − 0.12
≈ **39.9 ms** margin; if negative, renegotiate the SLA, shorten the path, or reduce
queueing (QoS/more capacity) — never "hope." **N-24.** (10−9.4)/10 = **6%**; legitimate
causes: TCP/IP+ACK overhead, or flow-control limits — not "link is broken" on its own.
**N-25.** Buildings: eight **/23s** (510 usable ≥ 500; over-provision 510/500 = 1.02 →
2%) = 8×512 = 4 096 addresses = **172.16.0.0/20**; links: 12 × /30 = 48 addresses →
one **/26** (172.16.16.0/26); reserves: 8 × /28 = 128 addresses → one **/25**
(172.16.16.64/25). Total 4 288 of 65 536. Worked building: 172.16.0.0/23, usable
172.16.0.1–172.16.1.254, waste 10 addresses [MC]. Alignment rule: the /26 must start
on a 64-boundary after the /20 — 172.16.16.0 qualifies.
