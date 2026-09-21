# LAB-04 Worksheet

Name: ________________  Date: ______  Due: L16 (per schedule)

## Pre-lab (hand answers)
1. Four /26s of 192.168.100.0/24: ________ ________ ________ ________ (usable each: ____)
2. /29 usable = ____ ; /30 usable = ____ ; /30 preferable when: __________________
3. 10.20.4.96/27 mask ________ ; range ________–________

## T1 — Drill table (hand first; then verified-by-Python ✓/✗ + correction)
| # | Hand answer (network/mask) | Python agrees? | If not, what was wrong |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

## T2 — Design table (state rule first!)
Headroom rule: ________________ VLSM order (largest first): ________________
| Function | Requirement (×headroom) | Chosen CIDR | Usable | Notes |
|---|---|---|---|---|
| staff | | | | |
| guests | | | | |
| printers | | | | |
| servers ×6 | | | | |
| p2p reserve | | | | |
Summary route to core: ________ Why exact: ______________________

## T3 — Verification record
Assertion snippet output (paste): ______________________________
Any overlap found? ______ How resolved: ______________________

## Post-lab (full answers in report)
1. Largest-first failure demo (smallest-first walk-through)
2. Headroom's price at the core + why summarization matters
3. When /30 p2p fails; the modern alternative + trade-off
