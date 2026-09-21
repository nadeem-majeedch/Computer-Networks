# LAB-01 — Instructor Guide

## Setup (before session)
- Two VMs on the host-only net (192.0.2.0/24), iperf3 installed. Test `iperf3 -s`/`-c` pair.
- Prepare offline bundle for accessibility route: a small TCP-transfer `.pcapng` + CSVs.
- Print worksheets; write gateway IP on the board.

## Solutions / expected values
- **Pre-lab 3:** one sample is noise; 20 samples give a spread (mdev) you can report honestly.
- **T1:** host-only LAN RTT typically 0.2–2 ms (virtualization adds jitter); internet RTT
  typically 10–100 ms. Students must report their own min/avg/max/mdev, not these ranges.
- **T2:** growth pattern (often +1–20 ms during load) = queueing at the bottleneck. On para-
  virtual NICs growth may be small — that's a valid finding if explained (buffering elsewhere).
- **T3:** VM→VM TCP commonly 1–10 Gbit/s depending on host CPU; UDP at 100 Mbit/s should
  show ~0 loss; `-b 0` may show loss (sender-limited) — good discussion point.
- **Post-lab 2:** queue ≈ extra_delay / (pkt_size/link_rate). With 1500 B on 1 Gbit/s:
  1 ms ≈ ~83 packets. Accept any stated assumption (L01 taxicab arithmetic).
- **Post-lab 3:** window ≈ throughput × RTT. E.g. 5 Gbit/s × 0.3 ms ≈ 187 kB; `ss -ti`
  shows `send <rate>bps` and cwnd estimates — comparing them is the analysis win.
- **Post-lab 4 (sample):** can't prove *why* (which hop) — no per-hop attribution from
  end-to-end RTT alone; can't prove causality of loss (UDP loss ≠ congestion proof).

## Common failure modes
1. iperf3 server on the wrong interface / already-running instance (`Address already in use`).
2. Students report only averages — remind them mdev is the jitter story (rubric: units, spread).
3. `-u` without `-b` misconception: UDP iperf3 default is 1 Mbit/s, not "max" — check they
   noticed the *reported* rate, not just the loss line.

## Grading notes (100-pt rubric, lab-strategy §6)
- Correct results (40): T1–T4 tables with units + all three iperf3 runs.
- Analysis (30): delay-component attribution with citations to their own numbers; BDP or
  window arithmetic attempted.
- Reproducibility (20): commands + environment table present (check_lab_env output pasted).
- Clarity (10): honest failure notes earn this; silent gaps lose it.
- Skip: challenge `​-P 4` analysis (recognition only).
