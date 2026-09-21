# PB-057 — The Outage Between Polls (L29, Intermediate)

| Field | Value |
|---|---|
| Difficulty | **Intermediate** |
| Lecture(s) | L29 — Monitoring, Telemetry & Systematic Troubleshooting |
| CLOs | CLO5 (detection-window arithmetic), CLO6 (monitoring design) |
| In-class slot | Main activity; 20 min, pairs |
| Case type | Calculation + design · Topic: Monitoring/operations |
| Evidence policy | Synthetic poll data, labeled; arithmetic desk-checked; sampling theorem intuition (no formal claims) |

---

## Student version

### Scenario
Users report "the ERP randomly hangs for a minute or two." The monitoring system —
which polls the ERP's interface counters every 5 minutes — shows the link at 100%
availability. The syslog (brought in later) disagrees.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system (illustrative):**

```
Polling: every 300 s, poller asks "is 10.20.80.10 SNMP-reachable?" (1 query)
Syslog (from the ERP switch, retrieved after user complaints):
  09:12:04  link down ( Gig0/1 )      09:13:31  link up     (87 s down)
  10:47:20  link down                 10:48:02  link up     (42 s down)
  13:01:55  link down                 13:03:28  link up     (93 s down)
User-visible impact: matches the syslog times (ERP reconnect storms)
Poller results at 09:10, 09:15, 10:45, 10:50, 13:00, 13:05: all "up"
```

### Problem statement
Compute why the poller misses every flap (detection probability), derive the poll
interval needed for 90%-detection of 87-second outages, and design the
syslog/event-based monitoring that replaces brute-force poll rate increases.

### Evidence pack
The labeled synthetic poll/syslog data. Facts: 300-s interval, single-query
reaches, three outages of 42–93 s, all missed. Assumption: outage timing uniform
relative to poll schedule (state it).

### Constraints
- Show the detection arithmetic for one outage (what must the poll instant land
  inside?).
- The syslog design must include *dedup/correlation* (a flapping port can emit
  hundreds of lines).

### Student questions
1. For one 87-s outage: what fraction of poll instants lands inside the down
   window? Compute the per-outage detection probability at 300-s polling.
2. All three outages missed: consistent with your Q1 arithmetic? (Show the joint
   probability.)
3. Poll interval for ≥90% per-outage detection of a 90-s outage — what's the
   interval, and what does that poll rate cost (queries/day, and what else breaks)?
4. Event-based design: what syslog pattern, dedup window, and alert rule replaces
   poll-rate increases? Name one failure mode that *polling* still covers better.

### Expected learning outcomes
- Quantify sampling-based detection of short outages.
- Recognize when event-driven telemetry beats polling (and when not).
- Design dedup/correlation for noisy event streams.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "A poll detects the outage only if its instant lands *inside* the down window.
   The window is 87 s wide; the schedule is 300 s apart."
2. "Three independent misses at p each — multiply. And beware: 'independent' is an
   assumption you must state."

### Solution
1. Detection requires the poll instant ∈ [down_start, down_end]: probability =
   87/300 ≈ **29%** per outage (uniform-timing assumption). Miss probability ≈ 71%.
2. Joint miss = 0.71³ ≈ **0.358** — i.e., missing all three has ~36% probability:
   entirely consistent with observation (not evidence of a broken poller — evidence
   of a *blind* design). State the independence assumption (flaps at different
   hours; poll schedule fixed ⇒ effectively independent).
3. Need interval I with 90/I ≥ 0.9 ⇒ I ≤ **100 s**. Cost: 86,400/100 ≈ 864 queries/
   day per device — cheap for one device, brutal across 500 devices (432k/day) and
   *still* misses the 42-s flap (42/100 = 42% detection). Polling can't buy this
   coverage at sane rates — the design conclusion, not a vendor gripe.
4. Event-based: watch for the syslog pattern `link down`/`link up` pairs on Gig0/1
   (and SNMP linkDown traps as the redundant channel ⚠ trap delivery is UDP —
   lossy; syslog over TCP preferred where available); dedup: group down/up pairs
   within 10 min into one *flap event* with count + duration; alert rule: ≥2
   flaps/10 min on one interface ⇒ page (correlate with ERP reconnect logs by
   timestamp). Polling still covers better: *silent* failures that generate no
   events (e.g., the device's management plane dying while the data plane lives —
   no syslog will ever arrive; a poll notices the silence). Hybrid: slow poll
   (5 min) as liveness + events for dynamics.

### Reasoning process
Facts: poll interval, outage durations, all-missed. Model: detection = instant ∈
window (uniform assumption); joint probability for multiple misses; event-driven
coverage independent of duration. Design conclusion: events for dynamics, polls for
liveness, dedup for noise.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Poll every 30 s" | Detection *would* succeed (87 s and 42 s both exceed 30 s), so the arithmetic isn't the problem — the cost is: 2,880 polls/day/device ⇒ ~1.4M queries/day across a 500-device fleet, for a problem that three syslog lines describe perfectly |
| "The poller is broken" | The joint-probability arithmetic says the misses were expected; blame the design, not the tool |
| "Trust syslog alone" | Syslog delivery is best-effort; a device that *stops logging* looks healthy — polls catch silence |
| "Alert on every syslog line" | A flapping port emits hundreds of lines — pager fatigue; dedup/correlation is the design work |

### Extension question
The switch starts emitting `linkDown` SNMP traps. Do traps replace syslog? Compare
on: delivery reliability, payload richness, and what happens when the *event*
channel itself is down. (Traps: UDP, unacknowledged (no inform retry unless
configured ⚠) — lossy exactly during network trouble; payload structured but thin
compared to vendor syslog detail; if the event channel is down, both are silent —
which is why the *slow poll* stays in the design as the liveness backstop. Answer:
complement, not replace.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Per-outage and joint arithmetic with stated assumptions; 100-s interval + fleet-cost disqualifier; event design with dedup and the polling's remaining niche |
| 3 Proficient | Arithmetic right; event design thin on dedup |
| 2 Developing | "Poll faster" without probability or cost |
| 1 Beginning | Blames the poller |

### References
- PD §9 / SNMP context ⚠ verify section mapping (course-text dependent)
- Kurose & Ross §9.3 (network management: SNMP polling vs traps)
