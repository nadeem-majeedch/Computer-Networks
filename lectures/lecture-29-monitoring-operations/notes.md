# Lecture 29 — Instructor Teaching Notes
## Monitoring, Telemetry & Systematic Troubleshooting (120 min)

| Field | Value |
|---|---|
| Status | Draft v0.1 — instructor review required |
| CLOs | CLO7 primary; CLO1 measurement rigor |
| Textbook anchor | PD §13 (selected); monitoring literature ⚠ instructor-assigned |

---

## 1. Objectives hook
Board: **"You can't manage what you can't measure — and you can measure
beautifully wrong."**

Hook (3 min): two graphs on screen — same service, one shows 100% "up" (ICMP
checks), the other shows users failing (HTTP error rate). "Both instruments
are correct. Which one answers the user's question?" — the lecture's thesis.

## 2. Minute plan

| Minutes | Segment | What happens |
|---|---|---|
| 0–8 | Recap + hook | L01 metrics recall; the two-graph paradox |
| 8–28 | Concept 1 | What to measure: availability, latency, utilization, errors — and their traps |
| 28–48 | Concept 2 | Active vs passive; probes (ICMP/HTTP), counters (SNMP, stats) |
| 48–58 | Concept 3 | Dashboards + alert thresholds; on-call reasoning |
| 58–63 | Break | — |
| 63–100 | GA-29 (dashboard build) | Pairs build + instrument a staged lab topology |
| 100–112 | Diagnosis panel | Two staged failures; teams call them from evidence |
| 112–120 | Summary + exit ticket | — |

## 3. Concept walkthrough

### 3.1 What to measure (20 min)
- **Availability:** success ratio; *trap* — ping-up ≠ service-up (L27's health
  check lesson expanded: probe at the service layer your users actually use).
- **Latency:** RTT/percentiles; *trap* — means hide tails; p50/p95/p99 and the
  tail problem (L01's delay components give the vocabulary).
- **Utilization:** bandwidth %; *trap* — 95th-percentile billing vs average;
  bytes vs packets (small-packet tax).
- **Errors:** drops, CRCs, retransmissions (L06/L19 tie-ins); *trap* — errors
  cause symptoms elsewhere; watch correlations, not single counters.
- **SLI/SLO vocabulary (named):** what you measure / target you promise —
  one sentence, no deeper SRE doctrine.

### 3.2 Active vs passive (20 min)
- **Active probes:** you generate traffic (ping, traceroute, HTTP checks,
  iperf for bandwidth) — repeatable, targeted, but adds load and may measure
  a different path (traceroute's L16 caveat: asymmetry, rate limits).
- **Passive counters:** you watch what flows (interface stats, SNMP, sflow/
  NetFlow *named*, retransmission counters) — true traffic, but only where
  you have a vantage point.
- **Interpretation discipline:** always name the vantage point ("measured
  *from where, to where, when*") — the L01 rule returns as an operations law.
- **Frequency & retention:** sampling intervals smooth or hide spikes; a
  5-minute counter can hide a 10-second storm (one worked example).

### 3.3 Dashboards & alerts (10 min)
- **Dashboard design:** one row per question, not per metric — "is the site
  up," "how slow," "how saturated"; the two-graph hook becomes the template.
- **Alert thresholds:** static vs anomaly-based; alert on *symptoms* users
  feel (service latency/error), not on *causes* you can't confirm (CPU)
  — CLO7 evaluation, stated plainly.
- **On-call reasoning loop:** signal → hypothesis → probe → confirm/kill —
  the L16 troubleshooting loop with instrumentation behind it.

### Reference diagram — Telemetry pipeline

```text
devices ──SNMP poll / flow export──→ collector ──→ TSDB ──→ dashboard
                                                     │
                                                     └→ threshold alert → on-call
```

## 4. Important definitions
Availability · Latency percentile (p95/p99) · Utilization · Error counter ·
SLI/SLO · Active probe · Passive counter · SNMP (named) · NetFlow/sFlow
(named) · Dashboard · Alert threshold (static/anomaly) · Vantage point.

## 5. Real-world examples
- **The pager that fired at 3 a.m. for 0.3% packet loss** — a cause-threshold
  alerting the class will critique (evaluation in action).
- **Cloud LB health checks** (L27) return: them failing *was* the passive
  counter; today students build the equivalent themselves.

## 6. Mathematical/technical example
Percentile arithmetic on a worked set: RTTs {10, 12, 12, 14, 18, 20, 25, 60,
110, 150} ms — mean ≈ 43 ms, p95 ≈ 150 ms; "mean hides the tail" is not
rhetoric, it's arithmetic students compute in Part A of the worksheet.

## 7. GA-29: dashboard build (37 min)
Staged lab topology (VMs per handout): a web server, a client, a "faulty link"
(tc/netem-style shaping or a firewall rule toggled by the instructor). Pairs:
(1) run active probes (ping/p99 script, HTTP check loop); (2) record passive
counters (interface stats before/after); (3) plot a 3-row dashboard (up, p95
latency, errors); (4) propose one alert threshold and defend it. ⚠ Verify
netem/shaping tooling and the toggle script on the image; handout carries the
exact commands and a blank dashboard template; LAB-14 extends this build into
the CS-04 capstone.

## 8. Common misconceptions

| Misconception | Debunk |
|---|---|
| "Ping success = service healthy" | Different layers; probe the layer you promise (SLI) |
| "Average latency describes users" | Tails dominate experience; use percentiles |
| "More dashboards = better operations" | Dashboards answer questions; questionless dashboards are wallpaper |
| "Alert on every threshold breach" | Symptom-based alerting; cause-thresholds page humans for nothing |
| "Counter over 5 minutes = traffic over 5 minutes" | Sampling hides bursts; state the interval (vantage+time discipline) |

## 9. Suggested practical demonstration
Live toggle: instructor flips the "faulty link" on and off while the class
watches the dashboard — errors and p95 move before "up" ever changes. The
hook's paradox, now caused in front of them. ⚠ Pre-verify the toggle script.

## 10. Classroom activities
- **Metric choice drill:** 8 scenario cards ("users complain checkout is
  slow," "the link bills at 95th"), teams pick metric + probe in 4 min.
- **Alert review panel:** three alert configs critiqued — one good, two
  pager-bait; students vote and justify (evaluation drill).

## 11. Problem-solving questions
1. p99 latency doubled but mean barely moved. What traffic shape explains it?
   (tail events: GC pauses, retransmit storms)
2. Your HTTP check succeeds from the LB but fails from userland. Name two
   vantage-point explanations (different path/NAT; TLS or DNS difference).
3. You must alert on one metric for the GA-29 service. Which, and what
   threshold? Defend against "alert on cause."
4. A 95th-percentile-billed link shows avg 200 Mbps but bills 900 Mbps.
   Construct the burst pattern that does this.
5. Counter shows retransmissions rising 10× with p95 flat. Hypothesize and
   name the probe that confirms/kills it.

## 12. Formative assessment (with answers)
- MCQ: An SLI is the ________; an SLO is the ________ → measurement; target.
- MCQ: p95 of {10,12,14,18,20,25,60,110,150,12} ms is closest to → **150** (or
  ~110 depending on convention — accept either with justification; state the
  convention used).
- MCQ: SNMP delivers ________ data → passive (counter).
- Short: why alert on symptoms? → users feel symptoms; causes are unconfirmed
  until probed.

## 13. Exit ticket
1. Mean vs p95: which reflects users and why? ________
2. Active vs passive: HTTP check = ________; interface counters = ________.
3. Your alert threshold and its justification: ________.

## 14. Anticipated difficulties
- The percentile concept is new to some students; Part A's arithmetic
  scaffolds it — walk the 10-element example on the board before release.
- GA-29's dashboard "plot" is intentionally low-tech (table + sparkline);
  resist tool rabbit-holes — the handout's template keeps pairs focused.

## 15. Instructor preparation checklist
- [ ] ⚠ Verify GA-29 fault toggle + probes on the image; reference dashboard
- [ ] Print handouts + blank dashboard templates; metric/scenario cards
- [ ] Board pre-write: two-graph paradox; SLI/SLO box; vantage-point law
- [ ] Coordinate LAB-14 handoff (CS-04 monitoring stage)

## 16. Timing fallbacks
The alert-review panel may compress to two configs; GA-29's passive-counter
step can shrink to before/after snapshots; the diagnosis panel is protected.

## 17. References
- PD §13 (selected); monitoring/SRE literature ⚠ instructor-assigned (verify
  citations before assigning); SNMP/NetFlow RFC names only (⚠ verify numbers).
- L01/L16/L27 notes for continuity; GA-29 handout; LAB-14 (CS-04).
