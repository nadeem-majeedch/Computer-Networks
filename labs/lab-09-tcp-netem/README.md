# LAB-09 — TCP Under Stress: Delay, Loss, Bandwidth (netem)

| Field | Value |
|---|---|
| Anchor lectures | L19 (flow & congestion control), L04 (measurement) |
| CLOs | CLO5 (build/measure), CLO6 (evaluate) |
| Assessment | Graded lab deliverable (individual; 15% pool) — report with graphs & interpretation |
| Mode / duration | Individual; 2-h session + 48-h window |
| Environment | Namespaces with a netem "impaired link" (route C); tools: `tc`, `iperf3`, `ss`, `tcpdump` |

## Learning outcomes
1. Impair a link with netem (delay, loss, rate) and *verify the impairment* rather than
   assuming it.
2. Measure TCP throughput/RTT under each impairment and explain the direction of the
   change with congestion-control arithmetic (L19: cwnd, ssthresh, AIMD).
3. Read live TCP state with `ss -ti` (cwnd, ssthresh, retransmits) and connect it to your
   iperf3 numbers.
4. Recognize the reordered-ACK pitfall: why loss measured at the receiver is not
   congestion proof (foreshadows LAB-10/11 design).

## Pre-lab
1. Write AIMD's two rules in one line each (L19).
2. Throughput ≈ window/RTT: with a fixed cwnd, what does +50 ms RTT do to throughput?
3. Why does 1% random loss hurt TCP *more* than the bandwidth cost of 1% retransmits?

## Topology (T0)

```
 [snd ns] ──veth── [rtr ns: tc netem on the r2s side] ──veth── [rcv ns]
                     (the "impaired" middle link)
```

### Build (20 min)
```bash
for n in snd rtr rcv; do sudo ip netns add $n; done
sudo ip link add s1 type veth peer name r1s; sudo ip link set s1 netns snd; sudo ip link set r1s netns rtr
sudo ip link add r2s type veth peer name c1;  sudo ip link set r2s netns rtr; sudo ip link set c1 netns rcv
sudo ip netns exec snd ip addr add 192.0.2.11/24 dev s1
sudo ip netns exec rtr ip addr add 192.0.2.1/24 dev r1s
sudo ip netns exec rtr ip addr add 192.0.3.1/24 dev r2s
sudo ip netns exec rcv ip addr add 192.0.3.22/24 dev c1
for i in s1 r1s r2s c1; do sudo ip link set $i up; done
for n in snd rtr rcv; do sudo ip netns exec $n ip link set lo up; done
sudo ip netns exec rtr sysctl -w net.ipv4.ip_forward=1
sudo ip netns exec snd ip route add default via 192.0.2.1
sudo ip netns exec rcv ip route add default via 192.0.3.1
```

## Tasks

### T1 — Baseline, then verify impairments (20 min)
```bash
# shape BOTH directions: a qdisc delays only the packets leaving that interface
sudo ip netns exec rtr tc qdisc add dev r2s root netem delay 50ms   # snd→rcv direction
sudo ip netns exec rtr tc qdisc add dev r1s root netem delay 50ms   # rcv→snd direction
sudo ip netns exec snd  ping -c5 192.0.3.22        # expect ≈ 100 ms round trip
sudo ip netns exec rtr tc qdisc change dev r2s root netem rate 10mbit delay 50ms
sudo ip netns exec rtr tc qdisc change dev r1s root netem rate 10mbit delay 50ms
```
**Expected observation:** ping RTT grows to ~100 ms (each direction crosses one 50 ms
qdisc). Side experiment worth reporting: remove the r1s qdisc and note RTT ≈ 50 ms —
a one-sided qdisc shapes one direction only. If numbers don't match the configured
impairment, fix the *impairment*, not the story — verifying the tool is part of the
graded discipline.

### T2 — Throughput vs delay (20 min)
Three iperf3 runs: no impairment / 50 ms / 100 ms (TCP). Record all three.
**Expected observation:** throughput falls as RTT rises at fixed window behavior —
throughput ≈ window/RTT. Compute the implied window for each run from `ss -ti` sampled
during the run (`sudo ip netns exec snd ss -ti dst 192.0.3.22`).

### T3 — Throughput vs loss (25 min)
`tc qdisc change dev r2s root netem delay 50ms loss 1%`, then 3%.
**Expected observation:** throughput collapse disproportionate to the loss ratio
(retransmit timeouts, cwnd cuts — AIMD's multiplicative decrease). Record `ss -ti`
retransmit counters and cwnd trajectory if visible; graph throughput vs loss (3 points
minimum) in the report.

### T4 — The reordered-ACK caveat (15 min)
`tc qdisc change dev r2s root netem delay 50ms 25ms` (jitter causes reordering).
Run iperf3; observe duplicate-ACKs/fast-retransmits in the capture or `ss -ti`.
**Expected observation:** throughput drops even though *nothing was lost* — reordering
fakes congestion signals. Two sentences: what this means for LAB-10/11's design (your
reliable-UDP protocol must not panic on reorder).

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| ping shows half the expected delay | only one direction's qdisc configured | netem shapes egress only — add the qdisc to **both** `r1s` and `r2s`; confirm with `sudo ip netns exec rtr tc qdisc show dev r1s` and `sudo ip netns exec rtr tc qdisc show dev r2s` |
| `Unknown qdisc` error | netem module unavailable in the kernel | Route A image ships it; on custom kernels `sudo modprobe sch_netem` |
| iperf3 numbers vary wildly between runs | CPU contention in the VM | close other jobs; report medians of 3, and say so |
| `ss -ti` shows nothing | filter mismatch | `ss -ti dst 192.0.3.22` from inside `snd` ns; run *during* the transfer |

## Post-lab questions
1. From T2's three runs: implied window each time (throughput × RTT). Did it stay
   constant? What does that say about what limited you?
2. T3: why is the loss→throughput curve convex downward (steep collapse)? Use AIMD's
   multiplicative decrease in the explanation.
3. T4's reordering: which congestion signal got faked, and what would a *better*
   reliable-UDP design use instead of pure duplicate-ACK counting?
4. One thing netem's rate emulation is *not* (vs a real bottleneck queue) — and how you
   saw that in your numbers.

## Challenge (ungraded)
Add `netem delay 50ms loss 0.5%` and compare CUBIC vs BBR (default vs `tc`-independent:
use `iperf3 -C bbr` if the kernel supports it ⚠) — report the throughput difference and
one-line mechanism note per algorithm. Behavior is kernel-dependent; document yours.

## Accessibility / low-resource alternatives
- Instructor-provided dataset: CSVs of the T2/T3/T4 runs (no root needed) + the raw
  `ss -ti` logs; all questions answerable from the data + one provided pcapng.
- Graphs may be replaced by precise ASCII/verbal trend descriptions (rubric accepts
  either; numbers must be cited).
- All CLI text; no GUI dependency.

## Safety notes
netem lives only on lab-internal namespaces. Never attach impaired links to shared
networks (syllabus-safety §3.1). High-rate UDP tests stay inside the namespace pair.
