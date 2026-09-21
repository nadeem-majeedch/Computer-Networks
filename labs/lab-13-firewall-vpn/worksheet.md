# LAB-13 Worksheet

Names (pair): ________________  ______  Date: ______  Environment table: ______

## Pre-lab
1. Which needs "established" and why: ______________________
2. VPN adds ______ ; does not protect against: ______________________
3. Default-deny design sentence: ______________________

## T1 — Before picture
Plaintext payload visible on WAN? ☐ (frame #: ____) — this is the "before" evidence.

## T2 — Policy pass/drop matrix
| Flow | Predicted | Observed | Rule responsible |
|---|---|---|---|
| hostA→hostB ping | | | |
| hostA→hostB iperf3 | | | |
| hostB→hostA ping | | | |
| anything else | | | |

Blocked-counter evidence (paste counter line): ______________________

## T3 — Established-rule experiment
Without the rule: request ______ ; reply ______ (why): ______________________
The check `ct state established` performs: ______________________

## T4 — VPN verification
Route from hostA to 10.0.20.10 goes via: ______ (command output: ______________)
WAN capture during tunnel traffic shows: ______________________
Inner headers visible? ☐ ; what still leaks: ______________________

## T5 — Policy justification table (graded deliverable)
| Rule | Purpose | Attack mitigated | Cost |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## Post-lab (full answers in report)
1. Which rule caught hostB's ping + evidence
2. Established check + one attack it cannot stop
3. VPN hides X, still visible Y (your capture)
4. Static-key vs TLS-mode (one +, one −)
