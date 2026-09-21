# LAB-01 — Latency & Throughput: Measure, Then Explain

| Field | Value |
|---|---|
| Anchor lectures | L04 (delay taxonomy, measurement discipline) |
| CLOs | CLO5 (build/measure), CLO6 (evaluate) |
| Assessment | Graded lab deliverable (15% pool; see [`../syllabus-safety.md`](../syllabus-safety.md) §2) |
| Mode / duration | Individual; 2-h session + 48-h window |
| Environment | Host Wireshark optional; VM (route A/B) or any Linux lab box |

## Learning outcomes
By the end of this lab you can:
1. Measure RTT, jitter, and TCP/UDP throughput with `ping`, `traceroute`, and `iperf3`,
   stating units and sample discipline (n runs, min/median).
2. Distinguish the four delay components (processing, queueing, transmission, propagation)
   in measured numbers, and identify which one dominates a given path.
3. Explain loaded-latency growth (queueing during `iperf3`) using your own measurements.
4. Produce a reproducible mini-report: exact commands, environment table, honest failures.

## Pre-lab (before the session; 15 min)
1. L04 defines RTT and the four delay components — write the transmission-delay formula
   (you will use it in T3).
2. Estimate (guess, with reasoning): RTT VM→gateway ___ ms; RTT VM→example.com ___ ms;
   VM→VM TCP throughput ___ Mbit/s. You will compare against measurements.
3. Why does `ping -c 20` beat a single `ping` for a report? (Answer in one sentence on the
   worksheet.)

## Tasks

### T1 — Baseline latency (15 min)
```bash
ping -c 20 '<gateway-ip>'          # e.g. 192.0.2.1 on the host-only net
ping -c 20 example.com
traceroute -n example.com        # -n: numeric, no DNS delays
```
Record min / avg / max / mdev for each. **Expected observation:** LAN RTT is single-digit
ms with small spread; internet RTT is tens of ms with larger spread. `traceroute` hop count
correlates with RTT growth (each hop adds a router). *These are typical shapes, not
guaranteed numbers — your report explains your own values.*

### T2 — Loaded latency (20 min)
Run `ping -c 60 <peer>` **while** `iperf3 -c <peer> -t 45` runs in a second terminal
(single stream). Compare pre-load vs during-load RTT distributions.
**Expected observation:** RTT grows during the transfer — the queue in the bottleneck
router/interface fills (queueing delay, L01's taxicab analogy). If you see no growth on a
VM→VM path, say so and propose why (e.g., virtualization buffering).

### T3 — Throughput, TCP vs UDP (25 min)
```bash
# on the peer VM:
iperf3 -s
# on your VM (three runs each, record all):
iperf3 -c '<peer>' -t 10                 # TCP, default
iperf3 -c '<peer>' -t 10 -u -b 100M      # UDP at 100 Mbit/s offered load
iperf3 -c '<peer>' -t 10 -u -b 0         # UDP "unlimited" (sends as fast as allowed)
```
**Expected observation:** TCP self-clocks toward the path's usable capacity; UDP at a fixed
bitrate reports loss/jitter the sender causes when it exceeds capacity. Compare your TCP
number with your T1 RTT using the bandwidth-delay-product idea (L04/L19 preview).

### T4 — See it on the wire (10 min)
While one iperf3 TCP run executes:
```bash
sudo tcpdump -i any -c 30 -nn "tcp port 5201"
```
Identify: the handshake (SYN, SYN/ACK, ACK), data segments, ACKs. Two-line description of
who sends what — full dissection is LAB-09/GA-18 territory.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| `ping` to gateway fails | host-only adapter down | `ip addr` — is the interface up? re-run setup §2 step 3 |
| iperf3 `connection refused` | server not running on peer | start `iperf3 -s` there; check firewall rules |
| UDP shows 100% loss | offered rate exceeds path by far / `0` misuse | drop `-b 0`, use `-b 100M`; note it honestly |
| traceroute all `* * *` | ICMP/UDP filtered on path | try `traceroute -I` (ICMP mode) if policy allows; report the filter as a finding |

## Post-lab questions (in the report)
1. Which delay component dominated each path? Cite your numbers.
2. Your loaded-RTT grew by X ms. Estimate the queue length in packets that implies
   (state assumptions: packet size, per-hop vs end-host queueing).
3. TCP achieved Y Mbit/s with RTT R. What window size does that imply
   (throughput ≈ window/RTT)? Does the math hold against `ss -ti` output if you capture it?
4. Name one thing your measurements **cannot** prove.

## Challenge (ungraded)
Add `-P 4` parallel streams to iperf3. Does aggregate throughput change? Explain with
congestion-window arithmetic (L19 preview).

## Accessibility / low-resource alternatives
- Offline bundle: instructor-provided `lab01-sample.pcapng` + pre-recorded ping/iperf3 CSVs —
  all four tasks work as guided analysis; T1–T3 questions unchanged.
- tshark replaces Wireshark GUI everywhere: `tshark -r lab01-sample.pcapng -c 30`.
- Screen-reader note: all checks here are text commands; no diagram-reading required.

## Safety notes
Passive capture only (syllabus-safety §3.3). iperf3 runs only VM→VM inside the lab net.
