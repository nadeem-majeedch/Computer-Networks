# PB-056 — The Destination That Wasn't There (L29, Beginner)

| Field | Value |
|---|---|
| Difficulty | **Beginner** |
| Lecture(s) | L29 — Monitoring, Telemetry & Systematic Troubleshooting |
| CLOs | CLO6 (monitoring design; probe vs telemetry), CLO5 (coverage reasoning) |
| In-class slot | Opening hook; 12 min, pairs |
| Case type | Diagnostic-conceptual · Topic: Monitoring/operations |
| Evidence policy | Synthetic dashboards, labeled; the *absence* of data is itself the evidence |

---

## Student version

### Scenario
At 02:14, the monitoring dashboard went quiet for the analytics cluster's metrics
— no errors, no alerts, just a flat line. At 07:30 the on-call found the cluster
*had* been down since 02:10: a failed maintenance script had blackholed the route to
the metrics endpoint's subnet. The dashboard "worked" all night.

**Synthetic evidence — prepared for this case; internally consistent; not from a live
system:**

```
02:10  maintenance script: "ip route del 10.20.60.0/24" (leftover cleanup line)
02:10+ cluster metrics exporter → 10.20.60.10:8443: packets die at the gateway
       (no route → ICMP unreachable from the gateway, exporter retries silently)
02:14  dashboard: metrics line goes FLAT (last value held; no error, no gap marker)
07:30  human checks: cluster's *service* port also unreachable from monitoring host
Alert config review:
  alert on "metric absent for > 10 min"   ← NOT configured
  alert on "metric > threshold"           ← configured (value-based only)
```

### Problem statement
Explain why a flat line hid an outage, distinguish value-based alerts from
presence-based alerts, and design the minimal monitoring change that catches this
class of failure — including where the probe must *run from*.

### Evidence pack
The labeled synthetic timeline. Facts: route deleted; exporter silent; dashboard
flat; no absence alert. The absence itself is the key evidence — teach reading
*missing* data.

### Constraints
- The fix must catch *this* failure class (monitoring path loss), not just this
  instance.
- The probe's vantage point must be justified (why not run it *on* the metrics
  server?).

### Student questions
1. What did the dashboard show from 02:14–07:30, and what did it *mean*? (Flat
   line vs zero vs gap — three different things.)
2. Why didn't the exporter's retries surface as errors anywhere? (Where do its
   failures go when the path is gone?)
3. Value-based vs presence-based alerts: what does each monitor, and which was
   missing here?
4. Design the fix: the probe (what it checks, from where, at what cadence), and
   the alert rule that fires on *absence*.

### Expected learning outcomes
- Read flat/zero/gap as three distinct signals.
- Explain why telemetry failures are silent from the *monitored* side.
- Design presence-based probes from an independent vantage point.

---
<!-- INSTRUCTOR-ONLY BELOW -->

## Instructor version

### Hints (release order)
1. "The dashboard didn't lie — it repeated the last truth it was told. What's the
   difference between 'value stayed the same' and 'no value arrived'?"
2. "The exporter knows it's failing. Its error messages travel on... which path?
   The one that's down."

### Solution
1. Flat line = "last received value held" (many systems hold/interpolate the last
   sample); zero = a real measurement of nothing; gap = honest absence. The
   dashboard showed flat because the pipeline *ingested nothing new* and the
   visualization held the stale value — ambiguous by design unless absence is
   explicit.
2. The exporter's retry/failure logs go to *its own* log sink — often shipped over
   the same broken path, or at best visible only if someone looks. Failure
   telemetry of a broken failure-reporting path is structurally silent (the
   can-you-monitor-the-monitor problem).
3. Value-based: "is the number within bounds?" — blind when no number arrives.
   Presence-based: "did *any* sample arrive in window W?" — exactly the missing
   alert. Also absent: path probes from an independent vantage point.
4. Fix: (a) a blackbox probe *from a different network segment* (e.g., the office
   LAN or a second site): `nc -z 10.20.60.10 8443` / TCP-connect check every 30 s —
   cadence ≤ the alert window (10 min) so absence is detectable within one window;
   must *not* run on the metrics server itself (it would pass while the path to
   *collectors* is broken — the vantage point must share the *monitored* path, not
   the *monitored host*); (b) alert rule: "no successful probe in 5 min" AND
   "exporter metrics absent 10 min" ⇒ page. Both rules together distinguish
   exporter-dead from path-dead (two independent signals).

### Reasoning process
Facts: route deletion, silent exporter, flat dashboard, no presence alert. Model:
telemetry pipeline = producer → path → collector; failure at any stage is invisible
to value-based alerts; independent-vantage presence probes cover path failures.
Fix targets the missing signal class.

### Common incorrect approaches
| Approach | Why it's wrong |
|---|---|
| "Add more metrics" | More values, same blindness: absence is invisible regardless of metric count |
| "Alert on flat lines" | Ambiguous — flat can mean genuinely stable; presence/expiry semantics are the correct tool |
| "Probe from the metrics server" | Tests the wrong path; the server can answer locally while every collector is blackholed |
| "Check the dashboard hourly" | Toil, not telemetry; the 10-min absence alert already beats a human's cadence |

### Extension question
The probe itself now runs from the office LAN — which shares the *internet edge*
with... nothing else monitored. What coverage hole remains, and what's the
two-probe pattern that closes it? (If the office LAN's own path to the cluster
fails, the probe goes silent *with* the metrics — indistinguishable from cluster
down. Two probes from *diverse* vantage points: probe A (office) and probe B
(second site/VPN) — alert only when *both* fail (majority/quorum), distinguishing
cluster-down from vantage-down. Classic N+1 monitoring design.)

### Assessment rubric
| Level | Descriptor |
|---|---|
| 4 Exemplary | Flat/zero/gap distinguished; structural silence of failure-telemetry explained; probe vantage justified against the monitored path; two-signal alert design |
| 3 Proficient | Presence-alert fix right; vantage reasoning partial |
| 2 Developing | "Add an alert" without the absence/presence distinction |
| 1 Beginning | "The dashboard was broken" |

### References
- PD §9 operations/monitoring context ⚠ verify section mapping (course text
  dependent)
- Kurose & Ross §9.3 (network management SNMP context) ⚠; SRE practice (probe
  vantage, multi-window alerts) as general reference ⚠
