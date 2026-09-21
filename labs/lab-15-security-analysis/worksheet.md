# LAB-15 Worksheet (optional; recognition only)

Names (pair): ________________  ______  Date: ______
Topology verified by instructor before T3: ☐ (initials: ____)

## Pre-lab
1. SYN scan sends ______ ; open: ______ closed: ______ filtered: ______
2. ARP spoof: the lying packet is ______ ; victim caches: ______________________
3. TLS turns MITM into: ______________________

## T1 — Attacker view (contained)
| Port state | Packet pattern observed |
|---|---|
| open | |
| closed | |
| filtered | |

## T2 — Defender view
Footprint (from capture): ____ SYNs / ____ s to ____ distinct ports; payload bytes: ____
Detection rule (words + threshold): ______________________
Fired? ☐ ; plausible false positive: ______________________

## T3 — ARP MITM before/after
| Phase | victim `ip neigh` (gateway → MAC) | page fetch went through spoofer? |
|---|---|---|
| defense off | | |
| defense on | | |

Defense used: ☐ static neigh ☐ bridge validation

## T4 — TLS boundary
From `lab15-tls-mitm.pcapng`: attacker still sees: ______________________
Cert validation result: ______________________

## T5 — Detection engineering
| Rule | TP on scan capture | FP on normal capture |
|---|---|---|
| R1 | | |
| R2 | | |

## Post-lab (findings page)
1. Worse FP profile + why
2. What your defense does not stop
3. Unavoidable attacker metadata in T4
4. Cheapest effective defense + its cost
