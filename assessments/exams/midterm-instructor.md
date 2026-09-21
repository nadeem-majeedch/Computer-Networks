# Midterm Examination — Instructor Key & Marking Scheme

| Field | Value |
|---|---|
| Access | Instructor only |
| Timing | W8, in lecture, 90 min (strategy §3.4) |
| Scheme | 60 marks: A 18 · B 24 · C 18. M = method mark, A = accuracy mark (marking guide §3) |
| Moderation | Second-marker sample per strategy §4; scheme annotated on returned scripts |
| Sample paper | Release one week prior: assemble from `review/review-m1..m3.md` items (formats rehearse, items differ by construction — no leaks) |

## Section A (18)

**A1 (b)** segment · **A2 (b)** after the source MAC · **A3 (b)** Time Exceeded ·
**A4 (b)** IP/port fields · **A5 (c)** link-local unicast · **A6 (b)** flood in VLAN.

Distractor note: all six have exactly one defensible answer; (d)-type distractors test
the classic confusions (NAT↔routing tables; 802.1Q in payload).

**A7 (2).** Separate TX/RX paths per port: simultaneous send/receive, no shared
medium → no collision to detect (M: separate paths or "no shared medium"; A: both
halves). **A8 (2).** Collision domain: one switched port/boundary; broadcast domain:
VLAN or router boundary — with one example each (1+1). **A9 (2).** Compensating
errors cancel in additive checksums; CRC's polynomial division detects all bursts <
degree (1 mechanism + 1 example). **A10 (2).** Discover (client has no address yet)
(1); broadcast so any server on the link may offer (1). **A11 (2).** Router picks the
most-specific matching prefix (1); default = /0 (1). **A12 (2).** Timeliness beats
completeness — a retransmitted audio sample is stale on arrival (1); app accepts
loss/reordering handling itself (1).

## Section B (24)

**B1.** (a) 1 022 (A1). (b) four /24s: 10.30.0.0, 10.30.1.0, 10.30.2.0, 10.30.3.0 —
ranges .0–.255 each (M1 ranges method, A1 all four correct). (c) /25 (126 ≥ 90)
(A1). (d) 10.30.3.0/24 (A1). (e) 255.255.252.0 (A1). (f) 10.30.0.0/21 (M1) — safe only
if no covered prefix is routed/announced more specifically elsewhere (A1).

**B2.** (a) 2 MB = 16.78×10⁶ bits ≈ 1.678×10⁷ bits; ÷2×10⁷ = **0.84 s**
(M1 conversion, A1). Accept 2×10⁶×8/2×10⁷ = 0.8 s if MB = 10⁶ bytes stated as
assumption — **either assumption is fine when stated**. (b) +0.06 s → **0.90 s**
(or 0.86 s under decimal-MB assumption) (A1, consistency with (a) required). (c)
10⁶ × log₂101 ≈ **6.66 Mb/s** (M1 formula, A1 value). (d) 3×10⁵ ÷ 2×10⁸ = **1.5 ms**
(A1; accept 3.0 ms if RTT misread once, flagged).

**B3.** (i) After A's frame: `a1 → port 1` (learned from source) (1); m9 unknown →
flooded out ports 2–4 (1). After m9's reply: `m9 → port 3` (1); subsequent frames to
m9 go only to port 3 (1). (ii) 10.4.8.7 → **local**; 10.4.9.1 → **R2** (/16 beats /8);
10.7.2.2 → **R1** (/8 beats default) (1 each); rule: **longest-prefix match** (1).

## Section C (18)

**C1.** (i) 10.20.1.35 / MAC 9c:b6:d0:aa:bb:17 (1+1). (ii) Off-subnet destination →
frame addressed to the default gateway; MAC changes per hop, IP dst survives end-to-end
(2). (iii) TTL 62 vs initial 64 → **2 routers** (1 + 1 justification). (iv) Source
IP:port → public IP:port (translated); NAT records inside↔outside mapping + protocol +
timeout so the reply returns (1+1+1).

**C2.** (i) SYN t=0.000 → SYN,ACK t=0.055 → **RTT ≈ 55 ms** (1 + 1 for pair named).
(ii) **ack = 4001** (3000 + 1 SYN + 1000 data) (M1 arithmetic, A1 value, 1 meaning:
"next expected byte 4001"). (iii) Supports: server-side stall or return-path problem
(no response while handshake worked) (2). Does **not** support: "client path broken"
— the handshake completed both directions 55 ms earlier (2).

## Grade-boundary note

Marks are out of 60. Strategy §4's letter bands are **proposed** and pending
institutional mapping — convert only after faculty sign-off (assessments/README §4).

## Post-exam actions

1. Second-marker sample: 10% of scripts + all 58–60 and 0–15 boundary scripts.
2. Annotate scripts with M/A marks so feedback is diagnostic (marking guide §5).
3. Log any misprint/ambiguity and apply the *fair-to-everyone* fix before return.
