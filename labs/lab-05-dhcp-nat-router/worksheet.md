# LAB-05 Worksheet

Names (pair): ________________  ______  Date: ______  Environment table: ______

## Pre-lab
1. DORA order + who broadcasts each: ______________________________
2. NAT rewrites ______ and ______ ; remembers the ______ to reverse replies
3. DHCP needs broadcast at discovery because: ______________________

## T0 — Build record
Namespaces + links created (list commands that errored, if any): ______________
`ip_forward` value: ______

## T1 — DHCP server
Config used (paste `dhcp-range` line): ______________________
Lease file line after grant: ______________________
Client tool that worked: ☐ udhcpc ☐ dhclient ☐ python scaffold

## T2 — DORA annotation
| Message | From (MAC/IP) | To (MAC/IP) | Opt 53 |
|---|---|---|---|
| Discover | | | |
| Offer | | | |
| Request | | | |
| Ack | | | |

Which two were broadcast, and why: ______________________

## T3 — NAT translation pair
| Capture | Source seen | ICMP id |
|---|---|---|
| inside (r-c) | | |
| outside (r-w) | | |

## T4 — Lease table
Expiry / MAC / IP / hostname from your file: ______________________

## Post-lab (full answers in report)
1. Two changed fields, one constant (same-packet proof)
2. Why Ack broadcast here; when renewal is unicast (L22)
3. Reply-path problem without state
4. T1 50% with server down (L22 lifecycle)
