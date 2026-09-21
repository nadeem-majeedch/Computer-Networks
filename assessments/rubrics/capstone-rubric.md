# Capstone Rubric (CS-04, Team of 3–4)

| Field | Value |
|---|---|
| Weight | 15% of course (proposed plan) — stage weights within the 15% below |
| Scenario | Meridian Systems CS-04 (see [`../../docs/case-study-strategy.md`](../../docs/case-study-strategy.md) §2/§5) |
| Stages | Design doc W13 (25%) · build demo W15 (20%) · monitoring dashboard + data W16 (20%) · final report W16 (20%) · defense W16 (15%) |
| Governance | Team mark per stage, adjusted by peer contribution factor ±10% (case-study-strategy §5); double-marking per strategy §4 |

## Stage 1 — Design document (25% of capstone)

| Criterion | Pts | Full-credit evidence |
|---|---|---|
| Requirements & scope | 6 | Host counts, roles, growth assumptions stated; scope boundaries honest |
| Addressing plan | 6 | VLSM with headroom; per-VLAN purpose; reservation logic visible |
| L2/L3 topology & redundancy | 5 | Diagram; failure-domain thinking (what dies when X dies) |
| Services & policy | 5 | DHCP/DNS placement; firewall matrix (zone→zone permits) |
| Verification plan | 3 | Concrete tests the build *will* run (failover, load, security) |

## Stage 2 — Working build demo (20%)

| Criterion | Pts | Full-credit evidence |
|---|---|---|
| Build matches design | 8 | Addressing/VLANs/routes live and match the W13 document (drift explained) |
| Verification executed | 7 | At least three planned tests actually run during demo, results shown live |
| Fault handling | 5 | One instructor-injected fault handled; recovery observed, not asserted |

## Stage 3 — Monitoring dashboard + measurement data (20%)

| Criterion | Pts | Full-credit evidence |
|---|---|---|
| Metric selection | 6 | Continuous + event metrics; layers named; alert thresholds baseline-derived |
| Dashboard function | 5 | Live or replayed data visible; panes map to design decisions |
| Baseline & incident record | 6 | Pre-incident baseline recorded; one incident replayed with before/after |
| Measurement hygiene | 3 | Sampling windows stated; no averaged-away tails (p95/p99 shown) |

## Stage 4 — Final report (20%)

| Criterion | Pts | Full-credit evidence |
|---|---|---|
| Design-vs-as-built account | 6 | Deviations from W13 documented with reasons |
| Results narrative | 6 | Verification results interpreted via mechanisms (not described only) |
| Evidence & reproducibility | 5 | Commands/filters/datasets included; peer-runnable |
| Writing quality | 3 | Structured, units, labeled figures |

## Stage 5 — Defense (15%)

| Criterion | Pts | Full-credit evidence |
|---|---|---|
| Presentation (≤ 15 min) | 5 | Clear narrative: requirements → design → evidence |
| Individual Q&A | 8 | **Each member** answers deep questions on their area; explainability rule enforced |
| Handling the unknown | 2 | "We don't know, here's how we'd find out" scores; bluffing does not |

## Peer contribution factor

Each member rates every member (including self) 0–10 on contribution and
explainability; instructor moderates. The factor shifts an individual's capstone mark
by **±10% of the capstone component** (strategy §3.7), documented in the course file.

## Integrity anchors

- Evidence reproducibility rule (integrity doc §2) applies to every stage — a
  dashboard showing data the build cannot produce is a Stage-3 zero.
- AI use: permitted for grammar/explanation only; graded design prose must be the
  team's (integrity doc §3, ⚠ VERIFY against program policy).
