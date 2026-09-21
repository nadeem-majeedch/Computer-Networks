# Weekly Quiz — Week 15 (L29, L30)

| Field | Value |
|---|---|
| Coverage | L29 — Monitoring & troubleshooting · L30 — Mobile & wireless enterprise networking |
| Mode | Formative, ~10 min, individual, open notes |
| Graded window | — |
| Key | fenced at end — do not distribute |

## Student questions

**Q1 [B|CLO4|L29]** Name two metrics a network monitoring system collects continuously,
and the layer each lives at.

**Q2 [I|CLO6|L29]** Give the course's troubleshooting order-of-operations (bottom-up vs
top-down decision) for: (a) "new server unreachable," (b) "app is slow but ping is
clean." One sentence each on why that direction fits.

**Q3 [I|CLO6|L29]** An alert fires on 90% link utilization at 03:00 nightly. What two
questions turn this alert into a decision, per L29's baseline concept?

**Q4 [I|CLO6|L30]** A phone on Wi-Fi walks from AP-1 (ch 36) to AP-2 (ch 36, same
SSID). What is this handover called, and why does the *client* make the choice?

**Q5 [I|CLO6|L30]** An enterprise WLAN serves 40 students in one room on one AP.
Beyond the 2.4 GHz channel plan, name the capacity concept that actually limits the
design, and one structural mitigation.

**Q6 [I|CLO6|L30]** Your laptop's Wi-Fi shows −50 dBm at the AP yet transfers crawl.
Why is signal strength alone insufficient to predict throughput? Name one coexisting
factor.

---

## INSTRUCTOR KEY — DO NOT DISTRIBUTE

**Q1.** Examples: link utilization (%) at L2/L3 (interface counters); RTT/latency at
L3–L7 (probes); packet loss; error counters at L2. Any two with correct layers. [B·CLO4]

**Q2.** (a) bottom-up: "unreachable" suggests a link/L3 fault — check physical/IP path
first (cheap, decisive). (b) top-down or app-centric: ping clean means path is up;
slowness likely lives above (server processing, TCP windowing, app chatter) — start
higher. [I·CLO6]

**Q3.** (i) Is 90% the *baseline* for 03:00 (scheduled backup job) — i.e., is this
normal-but-loud? (ii) What does the utilization *cost* (loss/latency during that window)
— i.e., is capacity actually insufficient? Baseline context converts a threshold into a
judgment. [I·CLO6]

**Q4.** Roaming (BSS transition). The client decides because the station controls its
own RF assessment (beacon/probe quality) — infrastructure can only nudge it (accept
"client-driven association" with correct rationale). [I·CLO6]

**Q5.** **Airtime contention**: 40 clients share one radio's airtime; per-client
throughput ≈ airtime share, not a channel split. Mitigations: add APs (cells) on
different channels, or move to 5/6 GHz with more channels. [I·CLO6]

**Q6.** Throughput is set by *airtime quality and contention*, not raw signal: strong
signal can still coincide with co-channel interference, high client density, or poor
SNR from noise floor (−50 dBm RSSI says nothing about noise or channel busyness). One
named factor with mechanism suffices. [I·CLO6]
