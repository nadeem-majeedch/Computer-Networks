# LAB-02 Worksheet

Names (pair): ________________  ______  Date: ______  Environment table: ______

## Pre-lab
1. Unknown-destination frame → switch does: ______________________
2. Access ports send frames (tagged/untagged): ________ ; trunk carries ________ VLAN(s)
3. ARP between VLANs — predicted behavior and why: ______________________

## T0 — Plan record
| Host | VLAN | IPv4 | Bridge/port |
|---|---|---|---|
| h1 | | | |
| h2 | | | |
| h3 | | | |
| h4 | | | |

Commands that failed (if any) + exact error: ______________________________

## T1 — Connectivity pattern
| From→To | Result | Evidence (command + count) |
|---|---|---|
| h1→h3 (VLAN 10) | | |
| h1→h2 (cross-VLAN) | | |

## T2 — Learning/flooding evidence
- p-h2 capture during h1's ARP request: frames seen = ______ (why?)
- tr0 capture: vlan IDs seen = ______ ; FDB entries after ping: ______________

## T3 — Tag anatomy
- TPID = 0x________ ; VID in your captured frame = ______
- Access-port capture shows the tag? (yes/no) ______ Why? ______________________

## Post-lab (full answers in report)
1. Where the cross-VLAN ping dies and which layer is responsible
2. FDB before/after — relate to learn/forward/flood
3. What breaks if the trunk carries only VID 20
4. Why hosts never see tags on access ports
