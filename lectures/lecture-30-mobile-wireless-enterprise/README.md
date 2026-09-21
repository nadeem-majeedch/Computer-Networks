# Lecture 30 — Mobile & Wireless Enterprise Networking

| Field | Value |
|---|---|
| Module | 8 — Integration & Capstone |
| Depends on | L10 (Wi-Fi fundamentals), L11 (WPA2/802.1X in practice), L16 (routing & the IP model) |
| CLOs addressed | **CLO6** (primary), CLO2 (physical-layer thread) |
| Bloom level | C3–C4 (design application with evaluation) |
| Assessment artifact | Exit ticket; GA-30 campus wireless design worksheet |
| Lab | GA-30 (in-lecture); no numbered lab |
| Readings | KR 6.3–6.4 (skim); PD 2.7 |
| Prerequisites | [`prerequisites.md`](../../docs/prerequisites.md) entry skills; L10/L11 tooling |
| Materials | [Teaching notes](notes.md) · [Worksheet](worksheet.md) — instructor-facing notes include demo commands and answer keys |

## Key questions
- What actually happens when your phone "stays online" while you walk across campus?
- Why does TCP care whether your IP address changes — and how do enterprises avoid the problem?
- How do you design Wi-Fi *on purpose* (coverage, channels, authentication) instead of installing APs until it works?
- What do cellular generations (4G/5G) actually change, at headline level?

## What you should be able to do afterwards
- Explain handover/reassociation as a network event and name what breaks if the IP address changes mid-connection.
- Frame the mobility problem at layer 3 (Mobile IP idea) and contrast it with the enterprise answer: seamless L2 roaming that preserves the IP.
- Run a simple RF link budget (FSPL) and use a cell-edge target (−67 dBm) to reason about AP placement.
- Design a small-campus wireless plan: AP count/placement estimate, 2.4/5 GHz channel reuse, SSID + 802.1X/RADIUS authentication, guest isolation.
- Situate 4G/5G headlines (eMBB, URLLC, massive IoT) as service classes rather than marketing speed numbers.

## Materials
- [Teaching notes](notes.md) — includes GA-30 mechanics, link-budget arithmetic, answer keys
- [Worksheet](worksheet.md) — RF drills + GA-30 design grid + exit ticket
- Floor plan: Meridian Building B (from the CS-01 bundle); spectrum view from LAB-11 if available

## Homework / preparation for next lecture
- Skim KR 6.3–6.4; bring one question about enterprise Wi-Fi you could not answer from L10/L11 alone.
- Read the CS-04 brief before L31 — the design clinic starts immediately.
