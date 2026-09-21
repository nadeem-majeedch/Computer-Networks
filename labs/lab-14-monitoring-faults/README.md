# LAB-14 — Monitoring Dashboard & Fault-Injection Drill

| Field | Value |
|---|---|
| Anchor lectures | L29 (monitoring, telemetry, systematic troubleshooting) |
| CLOs | CLO6 (evaluate/troubleshoot), CLO7 (operations/security ops) |
| Assessment | Graded lab deliverable (pairs; 15% pool) — report + dashboard |
| Mode / duration | Pairs; 2-h session + 48-h window |
| Environment | Namespaces (reuse LAB-07/09 topologies); tools: `snmp` (snmpget), Python, `tcpdump`, `tc` |

## Learning outcomes
1. Collect telemetry from lab "devices": interface counters (SNMP-style polls via snmpget
   or a local agent) and flow-style records from captures.
2. Build a minimal time-series dashboard (Python + CSV/SQLite + matplotlib or ASCII chart)
   that shows a metric changing over time.
3. Run a controlled fault-injection drill (netem latency spike, firewall rule flip) and
   *detect* it from the dashboard, not from the terminal you caused it in.
4. Write a 1-page RCA: symptom → hypothesis → evidence → cause → fix, with timeline.

## Pre-lab
1. Polling vs streaming telemetry: one sentence each (L29).
2. What does an SNMP `ifInOctets` counter actually count, and why do you need deltas?
3. Your p95 latency "baseline" — why is p95 harder to fake than an average?

## Tasks

### T0 — Build on the known topology (15 min)
Reuse LAB-09's 3-namespace topology (cite the script). Start a background poller on the
router link: a 5-second loop capturing `ip -s link show r1s` counters into CSV — or, if
the image ships `snmpd`, poll `ifInOctets` with `snmpget -v2c -c public <rtr> IF-MIB::ifInOctets.N`
(⚠ agent availability is image-dependent; the `/proc`-based poller is the guaranteed path).

### T1 — Baseline (15 min)
Generate steady background traffic (`iperf3 -b 5m -u`), poll for 3 minutes, produce your
baseline chart: throughput estimate (counter deltas) vs time, and p50/p95 of `ping` RTT.
**Expected observation:** flat-ish baseline with noise; the *spread* is your reference
for detecting the fault later.

### T2 — Flow-style records (15 min)
From a 60-second tcpdump, produce a per-flow table (src, dst, bytes, start) using
`tshark -r ... -T fields -e ip.src -e ip.dst -e frame.len` piped through a small Python
aggregator (scaffold provided). Rank the top 3 flows. This is L29's "flows as data".

### T3 — Fault injection, blind (25 min)
Instructor (or a pair's *other* member, blind) injects one of: (a) `tc qdisc change ...
delay 80ms`, (b) a firewall drop on one flow, (c) a silent link down. The detector pair
must: notice from the dashboard (not the terminal), name the symptom, hypothesize,
verify with a targeted probe, and record the timeline. Swap roles and repeat once.
**Expected observation:** (a) shows in p95 RTT within one poll interval; (b) shows as
throughput loss + blocked counters; (c) shows as interface errors/absent counters —
each fault has a *signature*; name yours from your own data.

### T4 — RCA (20 min)
One page per fault: symptom (metric + time) → hypothesis (≥2, ranked) → evidence (probe
outputs, dashboard excerpt) → cause → fix/verify. Grade language, not drama: "hypothesis
ranked by cost-to-test" is the L29 method.

## Troubleshooting
| Symptom | Likely cause | Action |
|---|---|---|
| Dashboard flat through a fault | poller died / wrong counter | run the poll loop foreground for 30 s; check deltas ≠ 0 |
| snmpget times out | no snmpd in image | use the `/proc`/`ip -s` poller (by design the fallback is first-class) |
| p95 == p50 | too few samples | ≥ 100 samples per window; poll faster or longer |
| Flow table empty | capture filtered wrong | capture unfiltered for 60 s; filter in the aggregator |

## Post-lab questions
1. Each fault's signature: which metric moved first, and how fast (poll interval)?
2. Why did you need deltas rather than raw counters (T1)?
3. Your RCA's losing hypothesis: why did you rank it second, and what evidence killed it?
4. One thing your dashboard *cannot* tell you (and which instrument would).

## Challenge (ungraded)
Alerting: add a threshold rule (p95 > baseline+3σ for 2 consecutive windows) that logs an
alert line; demonstrate a true and a false alert.

## Accessibility / low-resource alternatives
- Dataset route: instructor CSVs (baseline + 3 faults) + capture files; T3/T4 become
  detection-from-data, same rubric. ASCII charts acceptable (matplotlib optional).
- Screen-reader note: ASCII/CSV pipeline is fully text-based; chart optional.

## Safety notes
Faults are injected only on lab namespaces by the designated person; no fault injection on
shared infrastructure (syllabus-safety §3.1/3.7).
