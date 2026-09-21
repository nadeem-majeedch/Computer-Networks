# LAB-11 Demo Sheet

Names (pair): ________________  ______  Demo slot: ______  Environment table: ______

## Pre-lab (before the demo slot)
1. Code + logs submitted the night before: ☐
2. Environment verified on the demo bench (`check_lab_env.py`): ☐ netem available: ☐
3. T2 gate rehearsed once end-to-end (sha256 pair): ☐

## T2 — Gate checklist (must pass before demo)
- [ ] 0% loss transfer completed, sha256 sender: ______________
- [ ] sha256 receiver identical: ☐
- [ ] Retransmit counter = 0 (or explained: ______________)

## T3 — Matrix, measured
| Cell (loss/reorder) | Wall time | Retransmits | sha256 match? |
|---|---|---|---|
| 0% | | | |
| 2% | | | |
| 5% + reorder | | | |

## T4 — Recovery log (server killed)
Timeline: timeout #1 at t=____ ; resend; ack; completion at t=____
Deadlock discussion (one line): ______________________

## Prediction vs reality (report table; demo shows worst cell)
| Cell | Δ time | Δ retransmits | Mechanism (one line) |
|---|---|---|---|
| 0% | | | |
| 2% | | | |
| 5% + reorder | | | |

## Post-lab (report appendix)
1. Prediction-vs-reality table completed (one mechanism line per cell): ☐
2. Amendments list matches `SPEC-AMENDMENTS.md`: ☐
3. Timer defense (spec value vs T4 log) written: ☐

## Q&A notes (demo)
Amendments logged: ______________________
Timer defense (spec value vs T4 log): ______________________
