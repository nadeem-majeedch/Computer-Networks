# LAB-06 Worksheet

Names (pair): ________________  ______  Date: ______  Environment table: ______

## Pre-lab
1. ULA prefix + host address: ______________________
2. NS type ____ ; NA type ____ ; solicited-node target: ______________________
3. Link-local begins with ______ ; used for: ______________________

## T0 — Build verification (`ip -br addr` paste, one namespace)
```
(paste here)
```
Four address classes present? v4 ☐ v6-ULA ☐ v6-LL ☐ lo ☐
The intentional typo you found: ______________________ How you found it: ______________

## T1 — NDP vs ARP (frame numbers from lab06 capture)
| | ARP | NS (135) |
|---|---|---|
| Rides on | | |
| Destination (L2) | | |
| Who wakes up | | |

Multicast MAC seen: ______ Derived from: ______________________

## T2 — Selection
Unforced pick: ______ ; forced v4 result: ______ ; forced v6 result: ______
OS/policy note (record what your box did): ______________________

## T3 — ICMPv6 details
Echo-request hop limit: ______ ; NDP needs ARP? ______ Frame #s: ______

## Post-lab (full answers in report)
1. Two structural differences + one similarity
2. Which family won unforced, per what preference
3. Why IPv6 needs no ARP at all
4. Where fe80:: appeared and why it cannot be removed
