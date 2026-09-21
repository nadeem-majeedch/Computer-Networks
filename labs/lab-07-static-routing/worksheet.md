# LAB-07 Worksheet

Names (pair): ________________  ______  Date: ______  Environment table: ______

## Pre-lab
1. The sysctl that makes a namespace route: ______________________
2. Traceroute's returned ICMP type: ____ ; what distinguishes hop 1 from hop 2: ______
3. /8 via A vs /16 via B → winner ______ ; rule: ______________________

## T0 — Predictions (write BEFORE applying routes)
| Node | Route I will add | Why (one line) |
|---|---|---|
| hostA | | |
| R1 | | |
| R2 | | |
| R3 | | |
| hostB | | |

Claim to verify: "R2 needs nothing" — evidence from its table: ______________________

## T1 — End-to-end connectivity
Result: ______ loss; if partial, which hop died and why: ______________________

## T2 — TTL evidence
| Direction (link side) | ICMP type | TTL | Source |
|---|---|---|---|
| request on r12a | | | |
| reply on r12a | | | |

Decrement point (one line): ______________________

## T3 — Traceroute dissection
| Probe | TTL | Time-exceeded source | OR final |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## T4 — LPM drill
`ip route get 10.0.2.10` output: ______________________
Why the /32 won: ______________________ One operational risk of more-specifics: ______

## Post-lab (full answers in report)
1. Where TTL decremented (device + step)
2. R2 knowledge here vs two-/25 growth
3. Who generates time-exceeded; how traceroute stops
4. /32 win mechanism + the risk
