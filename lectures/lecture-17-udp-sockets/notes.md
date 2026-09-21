# Lecture 17 — Instructor Teaching Notes
## UDP & the Transport Layer's Job (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO4/CLO5 primary; CLO6 supporting |
| Textbook anchor | KR §3.1–3.3; RFC 768; RFC 8085 |

---

## 1. Objectives hook
Board: **"UDP is 8 bytes of header and a shrug. It carries DNS, video calls, online
games, and the entire QUIC/HTTP3 stack. 'Best-effort + ports' — how is that enough?"**

Hook (2 min): live video call with one second of network "junk" injected vs the same
over TCP retransmitting an old frame — why does the video app *prefer* to drop?

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–6 | Recap + hook | L16 LPM recall; the video-vs-TCP thought experiment |
| 6–24 | Concept 1 | Transport's three jobs; multiplexing by ports; demux keys |
| 24–40 | Concept 2 | UDP header, checksum behavior, what UDP does NOT do |
| 40–55 | Concept 3 | When UDP; when to add reliability yourself (L20 preview) |
| 55–60 | Break | — |
| 60–72 | LAB-08 briefing | Skeleton walkthrough; milestones |
| 72–108 | LAB-08 (in-class) | Pairs build the UDP chat/file transfer |
| 108–118 | Demos + summary | 2 pairs demo; exit ticket |
| 118–120 | Preview | TCP next: "what would it take to fix all of UDP's gaps?" |

## 3. Concept walkthrough

### 3.1 The transport layer's three jobs (18 min)
1. **Process-to-process delivery.** IP delivers host-to-host; many processes share one
   host. **Ports (16-bit)** are the apartment numbers. **Demultiplexing** on arrival:
   - UDP demux key: 2-tuple (dst IP, dst port) — every datagram independent.
   - TCP demux key: **4-tuple** (src IP, src port, dst IP, dst port) — each connection
     identified by all four (two browsers tabs can both use src port 51000 to the same
     server because connections differ... careful: two tabs typically share one
     connection; better example: two different apps both connecting to the same
     server:443 from the same host get different ephemeral source ports — hence
     distinct 4-tuples).
   - **Ephemeral ports** (~49152–65535 client side) vs **well-known ports** (IANA:
     53 DNS, 67/68 DHCP, 123 NTP, 443 HTTPS, 1935 RTMP, 5060 SIP).
2. **(Optionally) Integrity checking.** UDP checksum over pseudo-header + header +
   data (1's complement; L06's checksum returns); optional in IPv4 (all-zeros =
   unchecked) but **mandatory in IPv6** (IPv6 has no header checksum — L15).
3. **(Optionally) Congestion control & reliability.** UDP does *neither*. That's not a
   defect; it's a *feature for apps that can outperform TCP's behavior* — but it
   imports obligations (RFC 8085's guidance: apps should implement congestion
   avoidance; say this explicitly — engineering ethics meets math).

### 3.2 The UDP header & what's absent (16 min)
| Field | Bits | Job |
|---|---|---|
| Source port | 16 | Return address (may be 0 for "no reply expected") |
| Destination port | 16 | Demux |
| Length | 16 | Header+data bytes (minimum 8) |
| Checksum | 16 | Integrity (optional v4; required v6) |

- No sequence numbers, no ACKs, no connection setup, no flow/congestion control, no
  ordering. Consequences demonstrated live: inject loss → video keeps playing but a
  sentence of chat vanishes; inject reordering → chat messages arrive out of order.
- **Multicast/broadcast capability** (UDP only): one-to-many without N copies (IPTV,
  service discovery) — a capability TCP structurally lacks.

### 3.3 When UDP; when to fix it yourself (11 min)
- Choose UDP when: latency > late data (voice/games/live video), one request/reply
  fits one datagram (DNS — L21), or you're building your own transport anyway (QUIC —
  L23/L20's project rationale).
- The obligation ladder (preview of L20): sequence → ACK → timeout/retransmit →
  in-order delivery → congestion control. Every rung is what TCP gives you; building
  it yourself is LAB-10/11's project — today the students only *name* the rungs.

### Reference diagram — UDP header (8 B) and demux

```text
    0                15 16               31
   ┌──────────────────┬──────────────────────┐
   │     src port     │       dst port       │
   ├──────────────────┼──────────────────────┤
   │      length      │      checksum        │
   └──────────────────┴──────────────────────┘
 socket bound *:53 receives every datagram with dst port = 53
```

## 4. Important definitions
Port · Well-known vs ephemeral ports · Multiplexing/demultiplexing · Demux keys
(2-tuple vs 4-tuple) · Datagram · Pseudo-header · Segment vs datagram ·
Connectionless · Multicast (capability note).

## 5. Real-world examples
- **DNS** is the every-day UDP app: one query, one reply, no ceremony (L21 shows the
  capture; TCP fallback for big/secure answers mentioned there).
- **Voice over Wi-Fi:** frame loss sounds like a *click*, not silence — concealment
  beats retransmission; exactly the UDP trade.
- **QUIC:** the entire HTTP/3 stack rides UDP — proof that "unreliable + ports" is a
  *platform*, not a toy.

## 6. Mathematical/technical example
Demux collision puzzle: two apps on one host both talk to server:443 simultaneously.
Kernel assigns ephemeral src ports 51000/51001 → two 4-tuples → no confusion. With
UDP (2-tuple demux): same dst port 5353 from two apps → replies indistinguishable →
why DNS resolvers use a single socket per resolver process (or why 2-tuple demux
works for request/response with matching transaction IDs — L21 previews).
Length/checksum arithmetic: datagram 1,500 B IP payload; UDP length = 8 + 1,472;
pseudo-header adds IPs (not transmitted) into the checksum.

## 7. LAB-08 briefing (12 min)
Skeleton (provided): `udp_server.py` (bind, recvfrom loop, decode) and
`udp_client.py` (sendto, recvfrom with timeout). Tasks: (1) echo chat both ways;
(2) file transfer with chunking (1,400 B chunks — MTU discipline from L12) and
per-chunk loss injection (`tc netem loss 5%` on one VM) — observe missing chunks;
(3) add per-chunk numbering (the first ladder rung!) — observe reordering under
`netem delay 50ms 25ms`; (4) stretch: simple stop-and-wait ACK. Demo at 10 minutes
before end of session. ⚠ Verify netem on image; skeletons pre-placed.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "UDP is broken/unreliable IP" | It's *exactly* IP + ports + optional checksum; absence of features is the design |
| "UDP doesn't check errors at all" | Checksum exists (mandatory in IPv6); it detects, never repairs (L06) |
| "Ports are cables/channels with reserved bandwidth" | Demux labels; no capacity is reserved |
| "UDP has no congestion control, so it's always faster" | It can be *worse*: loss without adaptation collapses throughput (L19 explains TCP's behavior; uncontrolled UDP harms everyone incl. itself) |
| "UDP can't be reliable" | You build reliability *over* it (L20; QUIC exists) |
| "The same src port from two apps confuses the kernel" | 4-tuple demux (TCP); 2-tuple (UDP) + app-level IDs handle it |

## 9. Suggested practical demonstration
`iperf3 -u` between VMs at increasing offered rates: watch the *loss line* climb while
TCP's report on the same path stays clean — UDP's indifference made numeric. Then the
netem loss demo inside LAB-08. ⚠ Pre-verify iperf3/netem on the image; keep rates
modest in a shared teaching network (politeness!).

## 10. Classroom activities
- **Demux debugging (5 min):** 6 weird scenarios (two apps, same port; reply to port
  0; length field lies) — classify "kernel handles / app handles / broken packet".
- **Loss-tolerance auction:** 5 app profiles (video call / bank transfer / game state /
  file sync / live scores ticker); teams bid which transport and which *rungs of the
  ladder* the app must implement itself.

## 11. Problem-solving questions
1. Server receives datagram to port 53 from two clients simultaneously (UDP). How are
   replies routed to the right client? (2-tuple demux + app transaction ID — DNS
   preview.)
2. Why is UDP checksum mandatory in IPv6? (No IP header checksum → last-resort
   integrity.)
3. Your file transfer over UDP loses 1 in 20 chunks at 5% injected loss — why not
   exactly 5%? (Independent loss per datagram vs chunk distribution — discuss.)
4. Estimate: 50 ms RTT, 1,400 B chunks, stop-and-wait — max throughput? (1,400×8/0.05
   = 224 kbps — motivates pipelining/windowing, L20.)
5. A game designer asks for "TCP but without the head-of-line blocking". Which rungs
   do they actually need? (Sequencing + selective ACK; not full ordering.)

## 12. Formative assessment (with answers)
- MCQ: UDP demux key is → **(dst IP, dst port)** 2-tuple.
- MCQ: UDP header bytes → **8**.
- MCQ: In IPv6, the UDP checksum is → **mandatory**.
- Short: name two things TCP provides that UDP doesn't, and one app for which the
  absence is *better*. → reliability/ordering; live voice (late data = useless data).

## 13. Exit ticket
1. UDP header field count and size: ________
2. Demux key for UDP: ________ (TCP: ________)
3. One rung of the "reliability ladder" and which module builds it: ________

## 14. Anticipated difficulties
- Students underestimate LAB-08's scope; the briefing's milestone table (with the
  demo checkpoint) keeps pairs realistic — enforce time checks.
- "Mandatory checksum in IPv6" collides with L15's "no checksum in IPv6" — say both
  facts together explicitly (header vs UDP-layer checksum).

## 15. Instructor preparation checklist
- [ ] ⚠ Verify skeletons + netem + iperf3 on image; test one full LAB-08 pass
- [ ] Print LAB-08 handouts; prepare loss-tolerance profile cards
- [ ] Board pre-write: header table; demux-key comparison; ladder rungs
- [ ] Check shared-network politeness (iperf rates; coordinate with room admin)

## 16. Timing fallbacks
Drop the demux-debugging activity; LAB-08 tasks 1–2 define the *minimum* demo
milestone — task 3–4 become homework if time collapses.

## 17. References
- KR §3.1–3.3; RFC 768 (UDP); RFC 8085 (UDP usage guidelines — cite for the
  congestion-obligation point).
- IANA port registry; Python socket docs; LAB-08 handout.
- ⚠ VERIFY editions/sections and image tooling this semester.
