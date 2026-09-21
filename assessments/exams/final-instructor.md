# Final Examination — Instructor Key & Marking Scheme

| Field | Value |
|---|---|
| Access | Instructor only |
| Scheme | 70 marks: A 21 · B 28 · C 21. M/A marks per marking guide §3; Ecf applies within a question |
| Verification | All numeric answers **[MC]** — reproduced by `tools/scripts/verify_assessment_numbers.py` |
| Moderation | Second-marker sample per strategy §4; double-mark C3 synthesis (two markers, mean if within 1 mark) |

## Section A (21)

**A1 (b)** QUIC over UDP · **A2 (b)** flow the firewall saw initiated · **A3 (b)**
cache duration · **A4 (b)** keeps forwarding by installed rules · **A5 (b)** unicast
renewal to original server · **A6 (b)** at the TCP layer.

**A7 (2).** Flow control protects the *receiver* (rwnd); congestion control protects
the *network* (cwnd) — 1+1. **A8 (2).** Self-built addresses may collide on the link;
DAD probes before use (M: collision possibility; A: probe-before-use). **A9 (2).**
Inside IP:port ↔ outside IP:port, protocol, timeout (any 3 of the tuple pieces +
timeout = full); removal: timeout expiry/close (1). **A10 (2).** Guarantees record
origin/integrity (signed zones) (1); does not stop, e.g., on-path interception *after*
resolution or malicious-but-legitimately-signed domains (1). **A11 (2).** The cert's
signer is not anchored in the client's trust store, so the name↔key binding is
unproven. **A12 (2).** Airtime (1); 60 clients share one radio's transmit opportunities
so per-client throughput ≈ goodput÷clients (1).

## Section B (28)

**B1.** (a) 2 046 (A1). (b) 10.0.0.0/22 (10.0.0.0–10.0.3.255) and 10.0.4.0/22
(10.0.4.0–10.0.7.255) (M1 + A1). (c) /26 (62 ≥ 60) (A1). (d) second subnet range
10.0.4.0–10.0.7.255; 200 ∈ [4,7].x → **yes** with range shown (M1 + A1).

**B2.** (a) 10⁹ × 0.04 = 4×10⁷ bits = **5 MB** (M1 + A1). (b) 1→2→4→8→16→32 = **5
RTTs** (A2). (c) ssthresh = 10, cwnd = 1 (A1 + A1). (d) implied window = 4×10⁶ × 0.05
= 2×10⁵ bits = **25 kB** (A1) — far below BDP (6.25 MB) → inspect the **window/rwnd
side first**, not the path (A1).

**B3.** (a) root → referral to `.edu` TLD servers (1); `.edu` → referral to
`example.edu` nameservers (1); authoritative → A/AAAA answer for `cs.example.edu`
with TTL (1). (b) At T2: broadcast for any server (1); at expiry: stop using the
address, re-enter discovery (release→init) (2).

**B4.** (a) **Denied** by rule (1) (1); principle: first-match ordering — broader
allows never see packets a prior deny caught (1); the fix (reorder or scope rule 1)
earns nothing extra but note it in feedback. (b) Policy includes both
10.20.0.0/22 ↔ 10.30.0.0/24 as selectors (1); visible: outer tunnel headers — public
IPs, timing/volume (1); inner payload encrypted (1); does not authenticate: endpoint
users/apps — machine/network-level only (1).

## Section C (21)

**C1.** (i) seq=2460 (1); convicted by the repeated `ack=2460` — every later segment
(3920, 5380, 6840) arrived, so the hole is 2460 (1). (ii) **Fast retransmit** (1) —
3 duplicate ACKs (the 0.052/0.054/0.056 triple after the original 0.050 ACK) (1);
fired before the RTO, which is the point of the mechanism (1). (iii) ack=8300 asserts
"bytes through 8299 received — next expected 8300" (1); proves the receiver buffered
3920/5380/6840 out of order and completed the stream once 2460 landed (1). (iv)
t=0.057 (retransmit) → t=0.107 (ACK) → **RTT ≈ 50 ms** (1 + 1 pair named).

**C2.** (i) ARP (1); DNS (1); TCP (1) — order counts; (ii) any four facts, 1 each:
ARP proves the gateway is on-link and reachable at L2 · DNS proves name→10.50.7.9
mapping from the local resolver · TTL-carrying A record implies caching rules · SYN
proves the client initiates toward the resolved address (dst IP 10.50.7.9) · seq=0
marks the ISN (raw capture convention). Any four with correct mechanism.

**C3.** Six decision points, 1 each, order-dependent (Ecf one slot): DNS resolution
via permitted resolver · ARP for the inter-VLAN gateway (L2 handoff) · inter-VLAN
firewall policy (permit 443) · routing to the servers' VLAN · TLS handshake
validating the *internal* name/cert · application serving the request. Award 1/6 for
correct set with wrong order; 6/6 only with correct order.

## Grade-boundary note

Marks out of 70; letter-band conversion pending institutional mapping (README §4).

## Post-exam actions

1. Second-marker sample 10% + boundaries; double-mark C3.
2. Annotate scripts with M/A marks; return within 2 weeks (strategy §6).
3. Log any ambiguity and apply the fair-to-everyone fix before return.
