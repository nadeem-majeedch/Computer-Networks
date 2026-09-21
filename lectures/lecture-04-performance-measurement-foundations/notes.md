# Lecture 04 — Instructor Teaching Notes
## Performance Lab Foundations: Measuring the Network (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO4/CLO5 primary; CLO6 introduced |
| Textbook anchor | KR §1.4; PD §1.5 |

---

## 1. Objectives hook
Board: **"'The network is slow.' Your first professional job is to replace that sentence
with three numbers and a command line."**

Hook (2 min): show two `ping` outputs side by side — 2 ms LAN vs 240 ms 4G — and ask what
each *proves* and what it *doesn't*.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–7 | Recap + hook | L03 journey recall (1 item); hook pings |
| 7–22 | Concept 1 | Measurement discipline: estimates, units, context, reproducibility |
| 22–40 | Concept 2 | `ping` mechanics (ICMP echo preview of L16) + pitfalls |
| 40–55 | Concept 3 | `traceroute` mechanics + caveats; `iperf3` model |
| 55–60 | Break | — |
| 60–75 | Instructor demo | Live `ping`/`traceroute`/`iperf3` on VM pair; interpret together |
| 75–105 | LAB-01 (start) | Students run the core measurement set in pairs |
| 105–115 | Compare results | Estimates vs measurements table on board; discuss deviations |
| 115–120 | Summary + exit ticket | LAB-01 completion instructions |

Note: this is a demo-led lecture — concept time is deliberately trimmed to give LAB-01 a
60-minute in-class start. Lab is *pedagogy* here, not an add-on.

## 3. Concept walkthrough

### 3.1 Measurement discipline (15 min)
- **Estimate first, measure second** (the estimation habit): every measurement should have a
  predicted value from L01 math; deviations are the lesson, not the number.
- Every number needs: **units** (ms vs Mb/s vs MB/s!), **direction** (up/down), **load
  context** (idle vs busy hour), **sample size** (one ping tells you almost nothing),
  **command** (reproducibility rule from the assessment strategy).
- **What each tool actually does:**
  - `ping` — ICMP Echo Request/Reply (L16); measures **RTT + loss** for small packets.
    Does NOT measure bandwidth. Can be deprioritized or blocked; absence ≠ outage.
  - `traceroute` — exploits TTL: sends packets with TTL=1,2,3…; each router that decrements
    TTL to 0 returns ICMP Time Exceeded, revealing hop addresses. Measures **per-hop RTT
    growth**. Caveats: routers may not reply (stars), may rate-limit (fake latency), and
    return paths differ (asymmetric) — the address you see is the *inbound* interface.
  - `iperf3` — pushes TCP (or UDP) streams between two endpoints; measures **achievable
    throughput** on the path, i.e., the bottleneck including both hosts' stacks — not the
    "capacity" of any single link.
- **Simplified teaching model flags:** ICMP behavior is sketched here; the protocol details
  (types, codes, checksums) land in L16. `iperf3` single-stream underestimates paths with
  high RTT×loss products — L19 explains exactly why (window-limited throughput).

### 3.2 Interpreting numbers (15 min)
- **Load-dependent RTT:** ping a gateway at 3 am vs during an exam hall's Netflix: queueing
  delay appears in the RTT. Loaded vs unloaded latency is *the* number modern speed tests
  report; we formalize it as queueing in L19 (bufferbloat).
- **Samples and statistics:** min/median/max matter; min ≈ propagation+transmission floor;
  median is representative; max reveals queueing spikes or loss retransmit effects.
- **Throughput vs capacity, again:** 940 Mbps on a "1 Gbps" LAN ≈ line rate minus
  Ethernet/TCP-IP overhead (inter-packet gap, preamble, ACKs) — compute: 1500 B payload per
  ~1538 B on wire ≈ 97.5% ceiling for packet efficiency alone; TCP adds ACK overhead both
  directions. Students should expect ~94–95% as "wire speed" for TCP with normal MTU.

### 3.3 A minimal measurement protocol (10 min)
The five-step habit students use in LAB-01 and every later lab:
1. State the question ("is the Wi-Fi bottleneck up- or downstream?").
2. Estimate from math (bottleneck? RTT? expected value + 20% tolerance).
3. Choose the tool that can *see* the quantity (RTT→ping; path→traceroute;
   throughput→iperf3; per-packet truth→Wireshark).
4. Run ≥3 trials, record commands verbatim, note time & conditions.
5. Interpret deviations: number > estimate? number < estimate? both instructive.

### Reference diagram — Bandwidth-delay product (the pipe model)

```text
sender ═════════════ pipe (the path) ═════════════ receiver
        │←── BDP = 10 Mb/s × 20 ms = 200 kb in flight ──→│
 throughput needs the pipe FULL: window ≥ one BDP + RTT
```

## 4. Important definitions
RTT · Throughput (achieved) vs capacity (available) · Bottleneck link · Baseline ·
Sample statistics (min/median/max) · Reproducibility (command + environment + time) ·
ICMP Echo · TTL · Rate limiting.

## 5. Real-world examples
- **Support ticket escalation:** the difference between "Wi-Fi is broken" and
  "RTT to gateway 4 ms idle / 220 ms loaded; loss 6% on 2.4 GHz channel 6 at 21:30" —
  one sentence converts an argument into a work order.
- **Cloud region choice:** ping your national cloud region vs a US region: physics again
  (L01 propagation), not marketing.
- **"Speed test says 300 Mbps but Steam downloads at 12 MB/s":** MB/s vs Mb/s (×8) plus
  server/CDN bottleneck — unit discipline saves embarrassment.

## 6. Mathematical/technical example
Estimate-then-measure worksheet example: VM-to-VM on a virtual switch (nominal 1 Gbps).
Expected RTT <1 ms (no propagation, no queueing at idle); expected iperf3 TCP ≈ 940 Mbps.
If students measure 300 Mbps → suspect the virtual bridge CPU limit — an *interpretation*
worth more than the number. For the campus→internet path: estimate RTT from distance
(600 km → ~6 ms floor) and compare.

## 7. LAB-01 core measurement set (demo + in-class run)
```bash
# 1) Baseline RTT to the default gateway (5 samples, machine-readable)
ping -c 5 $(ip route | awk '/default/ {print $3; exit}')
# 2) Path to a public site (record stars and note their meaning)
traceroute -q 1 example.com
# 3) Throughput, VM-to-VM (server on one VM, then test from the other)
iperf3 -s                     # on VM-B, leave running
iperf3 -c <VM-B-IP> -t 10     # TCP, 10 s
iperf3 -c <VM-B-IP> -t 10 -u -b 100M   # UDP at 100 Mbps: observe loss/jitter lines
# 4) The loaded-latency experiment (run iperf3 TCP in background, then ping again)
( iperf3 -c <VM-B-IP> -t 20 >/dev/null & ) ; ping -c 10 <VM-B-IP>
```
Interpretation questions are in the LAB-01 handout; the last experiment (queueing under
load) is the conceptual heart — connect explicitly to L01's ρ and forward to L19.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Ping measures speed (bandwidth)" | RTT of small packets; no data volume → no bandwidth information |
| "traceroute shows the return path" | Asymmetry: TTL expiry replies come back a different way; addresses are inbound interfaces |
| "A router that doesn't answer is down" | Rate-limiting/ICMP-depriority; forwarding continues |
| "iperf3 result = link capacity" | Achieved throughput of the path incl. host stacks & window limits (L19) |
| "One ping = a measurement" | Sample discipline; min/median/max tell different stories |
| "Mb and MB are interchangeable" | ×8 discipline; the Steam example |

## 9. Suggested practical demonstration
The §7 sequence live, projected, with pre-written expected outputs on a slide so deviations
are visible immediately. ⚠ Verify: both VMs on the teaching subnet, `iperf3` firewall rules
allow TCP 5201, campus uplink not saturated; if the room network blocks ICMP/UDP, run the
VM-internal set only.

## 10. Classroom activities
- **Estimate cards:** each pair gets a scenario (campus→google; VM→VM; phone→campus server)
  and writes estimates before any tool runs; we compare after LAB-01 runs.
- **Output diagnosis:** show 4 real (anonymized) tool outputs — one normal, one with loss,
  one rate-limited path, one asymmetric traceroute — pairs state what each proves.

## 11. Problem-solving questions
1. RTT to gateway: 0.4/0.5/0.4/3.1/0.5 ms. Interpret the 3.1.
2. iperf3 TCP: 940 Mbps on 1 GbE. Where did the missing 6% go?
3. iperf3 UDP at 200 Mbps on a path that delivers 95 Mbps: what does the receiver report?
4. Why can traceroute show hop 5 with *lower* RTT than hop 4?
5. Your estimate said 9 ms RTT; you measure 35 ms consistently. Give two hypotheses and a
   test for each. (Queueing on access link vs indirect routing/VPN.)

## 12. Formative assessment (with answers)
- MCQ: Which quantity does `ping` NOT provide? → **throughput**.
- MCQ: traceroute's mechanism relies on → **TTL expiry → ICMP Time Exceeded**.
- Short: why run iperf3 ≥3 times? → variance/queueing context; single run can coincide
  with a burst; reproducibility discipline.

## 13. Exit ticket
1. Tool for RTT / path / throughput: ________ / ________ / ________
2. Loaded latency is caused mainly by which delay component? ________
3. One thing you will do differently in every future lab report: ________

## 14. Anticipated difficulties
- VM networking problems consume pairs' time: TAs pre-verify one VM pair per bench;
  fallback script provided.
- Students over-trust single measurements: the loaded-latency experiment exists to shock
  that habit early.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify VM pairs communicate; iperf3 present on both; TCP/5201 allowed
- [ ] ⚠ Verify campus ICMP/UDP policy; prepare VM-internal fallback set
- [ ] Pre-compute expected outputs for this room (gateway IP, expected RTTs)
- [ ] Print LAB-01 handouts; ensure submission portal ready
- [ ] Prepare the 4 anonymized outputs for §10

## 16. Timing fallbacks
If VMs fail room-wide: instructor runs all commands on the projector; students complete the
interpretation columns from projected output. Never skip the loaded-latency experiment.

## 17. References
- KR §1.4; PD §1.5.
- iperf3 documentation (iperf.fr / GitHub esnet-iperf); iproute2 man pages (`ping` is from
  iputils; `traceroute` man page).
- RFC 792 (ICMP) — previewed; full treatment L16.
- ⚠ VERIFY tool versions on the semester VM image; record in the lab README.
